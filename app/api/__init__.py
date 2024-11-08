import os

from flask import Flask
from grants import grants_bp
from grants import SWAGGER_BLUEPRINT



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'gtp.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(grants_bp, url_prefix='/api')
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix='/swagger')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8085, debug=False)
