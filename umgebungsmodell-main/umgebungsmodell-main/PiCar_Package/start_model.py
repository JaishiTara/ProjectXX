from virtual_picar import application


app = application.App()


app.set_up_windows()
app.quit_program()

app.run_gui(False)