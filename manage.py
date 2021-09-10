from app.app import create_app, create_manager

app, socketio = create_app()
manager = create_manager(app)

if __name__ == "__main__":
    manager.run()


