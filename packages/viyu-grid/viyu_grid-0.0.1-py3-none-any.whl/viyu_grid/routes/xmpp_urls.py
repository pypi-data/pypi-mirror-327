# from typing import Type
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import class_mapper
# from .. import db_session, models

# def setup_grid_routes(xmpp):
#     """
#     Dynamically registers routes for each ORM model.
    
#     This function loops through all models defined in the `models` module and registers
#     dynamic GET routes that retrieve all records of the corresponding model.
    
#     Args:
#         xmpp: The XMPP (or any other server framework) instance where routes will be registered.
#     """
#     for model_name, model_class in models.items():
#         # Debugging: Log the type of model_class
#         print(f"[DEBUG] Checking model: {model_name}, Type: {type(model_class)}")
        
#         # Ensure the model_class is a valid ORM model class and not an instance or invalid type
#         if not isinstance(model_class, type) or not hasattr(model_class, '__table__'):
#             print(f"[WARNING] Skipping invalid model: {model_name}, Type: {type(model_class)}")
#             continue  # Skip invalid models
        
#         route_path = f"/{model_name.lower()}"
        
#         async def dynamic_get_handler(model=model_class):
#             """
#             Handles dynamic GET requests for retrieving all records of a given model.
            
#             Args:
#                 model (Type): The ORM model class.
            
#             Returns:
#                 dict: JSON response with status code and data/error message.
#             """
#             try:
#                 # Ensure the model has a `to_dict` method before calling it
#                 # if not hasattr(model, 'to_dict'):
#                 #     raise Exception(f"Model {model.__name__} does not have a 'to_dict' method.")

#                 records = db_session.query(model).all()
#                 if not records:
#                     return {"status": 404, "error": f"No records found for {model}"}
                
#                 # Use the `to_dict()` method of the model to serialize the data
#                 return {"status": 200, "data": [record.to_dict() for record in records]}
#             except SQLAlchemyError as db_err:
#                 return {"status": 500, "error": f"Database error: {str(db_err)}"}
#             except Exception as e:
#                 return {"status": 500, "error": f"Unexpected error: {str(e)}"}
#             finally:
#                 db_session.close()  # Ensure database session is closed after request
        
#         # Register the dynamic GET route
#         xmpp.add_get(route_path, dynamic_get_handler)
#         print(f"[INFO] Registered dynamic route: {route_path}")


def setup_grid_routes(xmpp):
    from .. import db_session, models

    # Register the static route for initializing the grid
    # xmpp.add_post("/initialize-grid", initialize_grid_handler)

    # Loop through each model and dynamically register routes
    for model_name, model_class in models.items():
        route_path = f"/{model_name.lower()}"  # Convert model name to lowercase for route

        async def dynamic_get_handler(request, model=model_class):
            """
            Handles dynamic GET requests for any registered model.
            """
            try:
                records = db_session.query(model).all()
                return {"status": 200, "data": [record.to_dict() for record in records]}
            except Exception as e:
                return {"status": 500, "error": str(e)}

        # Register dynamic GET route for each model
        xmpp.add_get(route_path, dynamic_get_handler)

        print(f"Registered dynamic route: {route_path}")  # Debugging log
