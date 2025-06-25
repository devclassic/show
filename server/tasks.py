from invoke import task


@task
def build(ctx):
    ctx.run("pyinstaller -F --collect-all funasr main.py")
