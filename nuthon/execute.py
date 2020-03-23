def execute(template, env):
    try:
        return eval(template, dict(env))
    except Exception as e:
        raise e