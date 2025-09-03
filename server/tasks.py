from invoke import task


@task
def build(ctx):
    cmd = "pyinstaller -F --clean --noupx --collect-all funasr --collect-all transformers main.py"
    ctx.run(cmd)
