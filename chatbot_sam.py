## Chat bot for crmnext.



__author__ = 'avi0gaur'


"""
    json pattern 
    eg:
    {
        "user_text":"Hi I lost my card",
        "user_name":"Avinash"
    }
"""
def run_bot(conv):
    """
        Thread starts from here.
        :return:
    """
    print(str(conv))
    txt = conv["user_text"]
    print(str(txt))
    return {"context": "lost card"}

if __name__ == '__main__':
    pass