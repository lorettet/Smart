
def errorJson(message='Une erreur est survenue'):
    return {'status':'error','message':message}

def successJson(message=''):
    return {'status':'success','message':message}
