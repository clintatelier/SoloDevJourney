import invoke

@invoke.task
def test(c):
    c.run("pytest")

@invoke.task
def lint(c):
    c.run("flake8 .")
    c.run("black --check .")
    c.run("mypy .")

@invoke.task
def format(c):
    c.run("black .")

@invoke.task
def check(c):
    lint(c)
    test(c)

@invoke.task
def run(c):
    c.run("python src/main.py")