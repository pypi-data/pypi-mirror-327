# viyu_grid/__init__.py

# Global variables to hold the database session and model classes
db_session = None
models = {}
xmpp_session = None

def validate_grid_config(GridConfig):
    """Validate the grid configuration."""
    if not isinstance(GridConfig, dict):
        raise ValueError("GridConfig must be a dictionary.")
    if not GridConfig.get("grid_name"):
        raise ValueError("GridConfig must contain a 'grid_name' key.")
    # Add any other necessary validations for GridConfig here

def validate_model_classes(model_classes):
    """Validate the model classes to ensure they are SQLAlchemy models."""
    if not isinstance(model_classes, dict):
        raise TypeError("model_classes should be a dictionary.")
    
    for model_name, model_class in model_classes.items():
        if not hasattr(model_class, '__tablename__'):
            raise ValueError(f"Model {model_name} is not a valid SQLAlchemy model class.")
        if not callable(model_class):
            raise ValueError(f"Model {model_name} is not callable and cannot be initialized.")
    
def initialize(xmpp, session, gridType, GridConfig, **model_classes):
    """
    Initializes the grid package with the database session and models.

    Args:
        xmpp (str): XMPP client or identifier.
        session (SQLAlchemy session): The SQLAlchemy session instance from main_server.
        gridType (str): Type of the grid.
        GridConfig (dict): Configuration related to the grid.
        model_classes (dict): A dictionary of model classes to register, e.g., Status=Status.

    This function:
        - Sets the global `db_session` variable.
        - Updates the global `models` dictionary with the provided models.
        - Imports and initializes the `db_handler` to avoid circular imports.
        - Prints the list of initialized model names.
    """
    global db_session, models, xmpp_session  # Declare xmpp as global before assignment

    try:
        # Validate inputs
        if not isinstance(gridType, str) or not gridType:
            raise ValueError("gridType must be a non-empty string.")
        
        # Validate GridConfig and model_classes
        validate_grid_config(GridConfig)
        validate_model_classes(model_classes)

        # Assign the session and update the models dictionary with provided model classes
        db_session = session
        models.update(model_classes)
        xmpp_session = xmpp  # Now we assign to the global xmpp variable

        # Log the initialized database session and models
        print(f"XMPP client: {xmpp_session}")
        print(f"Database session initialized: {db_session}")
        print(f"Grid initialized with the following models: {list(models.keys())}")

        # Fetch all records for each model for debugging purposes
        for model_name, model_class in models.items():
            print(f"Fetching all records for model: {model_name}")
            records = db_session.query(model_class).all()
            if records:
                print(f"Records found in {model_name}: {len(records)}")
            else:
                print(f"No records found in {model_name}.")

        # Import db_handler and setup routes only after models are initialized
        from viyu_grid.routes.xmpp_urls import setup_grid_routes
        setup_grid_routes(xmpp_session)

        # Additional grid initialization logic if necessary
        print(f"Grid type: {gridType}")
        print(f"Grid configuration: {GridConfig}")

    except Exception as e:
        print(f"Error during grid initialization: {e}")
        raise  # Re-raise the exception after logging it to propagate the error
