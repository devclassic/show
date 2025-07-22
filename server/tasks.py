from invoke import task


@task
def build(ctx):
    ctx.run("pyinstaller -F --noupx --collect-all funasr --collect-all transformers main.py")
