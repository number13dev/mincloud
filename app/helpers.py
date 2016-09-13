mimetypes = {"audio": """<i class="fa fa-file-audio-o fa-4x" aria-hidden="true"></i>""",
             "pdf": """<i class="fa fa-file-pdf-o fa-4x" aria-hidden="true"></i>""",
             "text": """<i class="fa fa-file-text fa-4x" aria-hidden="true"></i>""",
             "video": """<i class="fa fa-file-video-o fa-4x" aria-hidden="true"></i>""",
             }


def fa_mimetype(t):
    for k, v in mimetypes.items():
        if k in t:
            return v

    return """<i class="fa fa-file-text fa-4x" aria-hidden="true"></i>"""
