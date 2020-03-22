def execute(template, env):
    try:
        return eval(template, env)
    except Exception as e:
        raise e