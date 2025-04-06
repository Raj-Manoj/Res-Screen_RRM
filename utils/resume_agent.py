
def parse_resume(path):
    return {'name': path.split('/')[-1].split('.')[0], 'email': 'example@example.com'}

def match_candidate(jd_text, parsed_resume):
    return True
