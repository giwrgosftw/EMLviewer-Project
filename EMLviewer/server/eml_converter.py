from email import message_from_file
import os

# Path to directory where attachments will be stored:
STORE_PATH = "/tmp"


# To have attachments extracted into memory, change behaviour of 2 following functions:
def file_exists(f_name):
    # Checks whether extracted file was extracted before
    return os.path.exists(os.path.join(STORE_PATH, f_name).replace("\\", "/"))


# Saves cont to a file fn_name
def save_file(fn_name, cont):
    file_ = open(os.path.join(STORE_PATH, fn_name).replace("\\", "/"), "wb")
    file_.write(cont)
    file_.close()


# Constructs a filename out of messages ID and packed filename
# specifically multipart message filename, if there is one
# msg_id = .eml filename
# fn_name = packed filename (e.g. attachment's name)
def construct_name(msg_id, fn_name):
    msg_id = msg_id.split(".")
    # combined the parts without the dot "."
    # if the filename is e.g. "name.EML" will change to "nameEML"
    msg_id = msg_id[0] + msg_id[1]
    # if the attachment's name is e.g. "tool.pdf", it will return "nameEML.tool.pdf"
    return msg_id + "." + fn_name


# Removes double or single quotations
def rm_quot(str_):
    str_ = str_.strip()
    if str_.startswith("'") and str_.endswith("'"):
        return str_[1:-1]  # return the string without the 1st and last character/element
    if str_.startswith('"') and str_.endswith('"'):
        return str_[1:-1]
    return str_


# Removes < and > from HTML-like tag or e-mail address or e-mail ID
def rm_angle_brackets(str_):
    str_ = str_.strip()  # remove Leading and Trailing whitespaces
    if str_.startswith("<") and str_.endswith(">"):
        return str_[1:-1]
    return str_


def pullout(m_msg, key):
    """Extracts content from an e-mail message
    This works for multipart and nested multipart messages too
    m_msg  -- email.Message() or mailbox.Message() [e.g. structure tree from .eml]
    key    -- Initial message ID (some string) [e.g. name of the .eml file]
    Returns tuple(text_, html_, files_, parts_)
    text_  -- All text from all parts (are strings)
    html_  -- All HTMLs from all parts (are strings)
    files_ -- Dictionary mapping extracted file to message ID it belongs to
    parts_ -- Number of parts in original message
    """
    html_ = ""
    text_ = ""
    files_ = {}
    parts_ = 0
    if not m_msg.is_multipart():
        if m_msg.get_filename():  # It's an attachment
            fn_name = m_msg.get_filename()
            cfn = construct_name(key, fn_name)  # combined names
            files_[fn_name] = (cfn, None)  # adds the new name into the dict with key "fn_name"
            if file_exists(cfn):
                return text_, html_, files_, 1  # 1 = True = Part exist
            # payload returns the msg object as a string because is_multipart = false
            save_file(cfn, m_msg.get_payload(decode=True))  # decrypt
            return text_, html_, files_, 1
        # Not an attachment!
        # See where this belongs. text_, html_ or some other data:
        m_cp = m_msg.get_content_type()
        if m_cp == "text/plain":  # if it is text
            text_ += m_msg.get_payload(decode=True)
        elif m_cp == "text/html":  # if it is html
            html_ += m_msg.get_payload(decode=True)
        else:
            # Something else!
            # Extract a message ID and a file name if there is one:
            # This is some packed file and name is contained in content-type header
            # instead of content-disposition header explicitly
            m_cp = m_msg.get("content-type")

            # The root part that is usually the first one, references other parts
            # inline using their "Content-ID" parameter.This is how pictures are embedded into HTML.
            try:
                msg_id = rm_angle_brackets(m_msg.get("content-id"))
            except TypeError:
                msg_id = None
            # Find file name:
            name_idx = m_cp.find("name=")  # returns the lowest index of the substring "name="
            if name_idx == -1:  # Not found
                return text_, html_, files_, 1
            # create a new index which will be the lowest of the substring ";"
            # searching after the index "name_idx"
            semicolon_idx = m_cp.find(";", name_idx)
            if semicolon_idx == -1:
                semicolon_idx = None
            name_idx += 5
            # the name of the "something else" file belongs between the index name and semicolon
            fn_name = m_cp[name_idx:semicolon_idx]
            fn_name = rm_quot(fn_name)  # removes the quotation(s)
            cfn = construct_name(key, fn_name)  # combined names
            files_[fn_name] = (cfn, msg_id)  # add the new name with its id (coming from content-id)
            if file_exists(cfn):
                return text_, html_, files_, 1
            save_file(cfn, m_msg.get_payload(decode=True))
        return text_, html_, files_, 1
    # This IS a multipart message
    # So, we iterate over it and call pullout() recursively for each part
    itr = 0
    while 1:
        # If we cannot get the payload, it means we hit the end (no more parts):
        try:
            # payload returns the msg as a list of Message objects because is_multipart = true
            pl_msg = m_msg.get_payload(itr)  # iterate the list
        # Error if i<- or i>= number of items in the payload
        except (IndexError, TypeError):
            break
        # pl_msg is a new Message object which goes back to pullout
        t_part, h_part, f_name, p_msg = pullout(pl_msg, key)  # tuple
        text_ += t_part
        html_ += h_part
        files_.update(f_name)
        parts_ += p_msg
        itr += 1
    return text_, html_, files_, parts_


def caption(origin):
    """Extracts: send_to, send_from, subject_ and date_ from email.Message() or mailbox.Message()
    origin -- Message() object (structure tree from the .eml file)
    Returns tuple(send_from, send_to, subject_, date_)
    If message doesn't contain one/more of them, the empty strings will be returned
    """
    date_ = ""
    if origin.has_key("date"):
        date_ = origin["date"].strip()
    send_from = ""
    if origin.has_key("from"):
        send_from = origin["from"].strip()
    send_to = ""
    if origin.has_key("to"):
        send_to = origin["to"].strip()
    subject_ = ""
    if origin.has_key("subject"):
        subject_ = origin["subject"].strip()
    return send_from, send_to, subject_, date_


def extract(msg_file, key):
    """Extracts all data from e-mail, including send_from, send_to, etc., returns it as a dictionary
    msg_file -- A file-like readable object (e.g. the .eml file)
    key      -- Some ID string for that particular Message. (e.g. name of the .eml file)
    Returns dict()
    Keys: from, to, subject, date, text, html, parts[, files]
    Key files will be present only when message contained binary files
    """
    # If message is multipart, output dictionary will contain a key "files"
    # with all filename(s) of extracted other files that were not text or html.
    # That is a way of extracting attachments and other binary data.

    m_msg = message_from_file(msg_file)  # returns a message object structure tree from .eml
    send_from, send_to, subject_, date_ = caption(m_msg)  # tuple
    text_, html_, files_, parts_ = pullout(m_msg, key)  # tuple
    text_ = text_.strip()
    html_ = html_.strip()
    msg = {"subject": subject_, "from": send_from, "to": send_to, "date": date_,
           "text": text_, "html": html_, "parts": parts_}
    if files_:
        msg["files"] = files_
    else:
        msg["files"] = ""
    return msg


# Inputs the content of the dictionary into a string and returns it
def create_text(text_str, email_dict):
    from_ = email_dict["from"]  # inputs the dictionary's value with key "from" into the string
    to_ = email_dict["to"]
    subject = email_dict["subject"]
    parts = email_dict["parts"]
    date = email_dict["date"]
    txt = email_dict["text"]
    html = email_dict["html"]

    files = []
    # Iterating the whole dictionary with key "files"
    for iter_y in email_dict["files"]:
        files.append(iter_y)  # adds every single item into the files[] list

    text_str += "From: " + from_ + "\n"
    text_str += "To: " + to_ + "\n"
    text_str += "Subject: " + subject + "\n"
    text_str += "Date: " + date + "\n\n"
    text_str += "Attachments: " + ", ".join(files) + "\n"
    text_str += "Parts: " + str(parts) + "\n\n"  # converts parts to string
    text_str += "Text:\n\n" + txt + "\n\n"
    text_str += "HTML:\n\n" + html
    return text_str


# Converts the .eml file to .txt and extracts its attachments (if any) by using the above functions
def metamorphosis(filepath):
    nam = filepath[:-4]  # keeps the name without the format (".eml")

    f_eml = open(filepath, "rb")  # Open the .eml file in binary format for reading
    email_dict = extract(f_eml, f_eml.name)
    f_eml.close()

    text_str = ""
    text_str = create_text(text_str, email_dict)

    w_text = open(nam + ".txt", "w")  # create an empty .txt file
    w_text.write(text_str)  # input the .eml content (since now is a string) to the .txt file
    w_text.close()
