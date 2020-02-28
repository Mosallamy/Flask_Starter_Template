from starter import create_app

app = create_app()
app.app_context().push()
app.run(port=3400,debug=True)