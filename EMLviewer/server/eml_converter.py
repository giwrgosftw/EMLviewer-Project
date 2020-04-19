from email import message_from_file
import os

# Path to directory where attachments will be stored:
PATH = "/tmp"


# To have attachments extracted into memory, change behaviour of 2 following functions:
def file_exists(f_name):
    # Checks whether extracted file was extracted before
    return os.path.exists(os.path.join(PATH, f_name).replace("\\", "/"))


# Saves cont to a file fn_name
def save_file(fn_name, cont):
    file_ = open(os.path.join(PATH, fn_name).replace("\\", "/"), "wb")
    file_.write(cont)
    file_.close()


# Constructs a filename out of messages ID and packed filename
# specifically multipart message filename, if there is one
def construct_name(msg_id, fn_name):
    msg_id = msg_id.split(".")
    msg_id = msg_id[0] + msg_id[1]
    return msg_id + "." + fn_name


# Removes double or single quotations
def disqo(str_):
    str_ = str_.strip()
    if str_.startswith("'") and str_.endswith("'"):
        return str_[1:-1]
    if str_.startswith('"') and str_.endswith('"'):
        return str_[1:-1]
    return str_


# Removes < and > from HTML-like tag or e-mail address or e-mail ID
def disgra(str_):
    str_ = str_.strip()
    if str_.startswith("<") and str_.endswith(">"):
        return str_[1:-1]
    return str_


def pullout(m_msg, key):
    """Extracts content from an e-mail message
    This works for multipart and nested multipart messages too
    m_msg  -- email.Message() or mailbox.Message()
    key    -- Initial message ID (some string)
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
            cfn = construct_name(key, fn_name)
            files_[fn_name] = (cfn, None)
            if file_exists(cfn):
                return text_, html_, files_, 1
            save_file(cfn, m_msg.get_payload(decode=True))
            return text_, html_, files_, 1
        # Not an attachment!
        # See where this belongs. text_, html_ or some other data:
        m_cp = m_msg.get_content_type()
        if m_cp == "text/plain":
            text_ += m_msg.get_payload(decode=True)
        elif m_cp == "text/html":
            html_ += m_msg.get_payload(decode=True)
        else:
            # Something else!
            # Extract a message ID and a file name if there is one:
            # This is some packed file and name is contained in content-type header
            # instead of content-disposition header explicitly
            m_cp = m_msg.get("content-type")
            try:
                msg_id = disgra(m_msg.get("content-msg_id"))
            except TypeError:
                msg_id = None
            # Find file name:
            name_idx = m_cp.find("name=")  # index position of the substring "name=" (lowest)
            if name_idx == -1:  # find() method returns -1 if the value is not found
                return text_, html_, files_, 1
            semicolon_idx = m_cp.find(";", name_idx)
            if semicolon_idx == -1:
                semicolon_idx = None
            name_idx += 5
            fn_name = m_cp[name_idx:semicolon_idx]
            fn_name = disqo(fn_name)
            cfn = construct_name(key, fn_name)
            files_[fn_name] = (cfn, msg_id)
            if file_exists(cfn):
                return text_, html_, files_, 1
            save_file(cfn, m_msg.get_payload(decode=True))
        return text_, html_, files_, 1
    # This IS a multipart message
    # So, we iterate over it and call pullout() recursively for each part
    itr = 0
    while 1:
        # If we cannot get the payload, it means we hit the end:
        try:
            pl_msg = m_msg.get_payload(itr)
        except (IndexError, TypeError):
            break
        # p_msg is a new Message object which goes back to pullout
        t_part, h_part, f_name, p_msg = pullout(pl_msg, key)
        text_ += t_part
        html_ += h_part
        files_.update(f_name)
        parts_ += p_msg
        itr += 1
    return text_, html_, files_, parts_


def extract(msg_file, key):
    """Extracts all data from e-mail, including send_from, send_to, etc., returns it as a dictionary
    msg_file -- A file-like readable object
    key      -- Some ID string for that particular Message. Can be a file name or anything.
    Returns dict()
    Keys: from, to, subject, date, text, html, parts[, files]
    Key files will be present only when message contained binary files
    For more see __doc__ for pullout() and caption() functions
    """
    # If message is multipart, output dictionary will contain a key "files"
    # with all filename(s) of extracted other files that were not text or html.
    # That is a way of extracting attachments and other binary data.
    m_msg = message_from_file(msg_file)
    send_from, send_to, subject_, date_ = caption(m_msg)
    text_, html_, files_, parts_ = pullout(m_msg, key)
    text_ = text_.strip()
    html_ = html_.strip()
    msg = {"subject": subject_, "from": send_from, "to": send_to, "date": date_,
           "text": text_, "html": html_, "parts": parts_}
    if files_:
        msg["files"] = files_
    else:
        msg["files"] = ""
    return msg


def caption(origin):
    """Extracts: send_to, send_from, subject_ and date_ from email.Message() or mailbox.Message()
    origin -- Message() object
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


if __name__ == "__main__":

    for i in os.listdir("."):
        if i.endswith(".eml"):
            nam = i[:-4]

            f = open(i, "rb")
            email_dict = extract(f, f.name)
            f.close()

            text_file = ""

            from_ = email_dict["from"]
            to_ = email_dict["to"]
            subject = email_dict["subject"]
            parts = email_dict["parts"]
            date = email_dict["date"]
            txt = email_dict["text"]
            html = email_dict["html"]

            files = []
            for y in email_dict["files"]:
                files.append(y)

            text_file += "From: " + from_ + "\n"
            text_file += "To: " + to_ + "\n"
            text_file += "Subject: " + subject + "\n"
            text_file += "Date: " + date + "\n\n"
            text_file += "Attachments: " + ", ".join(files) + "\n"
            text_file += "Parts: " + str(parts) + "\n\n"
            text_file += "Text:\n\n" + txt + "\n\n"
            text_file += "HTML:\n\n" + html

            wf = open("/tmp/" + nam + ".txt", "w")
            wf.write(text_file)
            wf.close()
