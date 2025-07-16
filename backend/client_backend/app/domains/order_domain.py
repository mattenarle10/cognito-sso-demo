class OrderDomain:
    """
    domain for order-related business logic
    handles jwt validation and order retrieval flow
    """
    
    def __init__(self, order_repository, jwt_service):
        """
        initialize order domain
        
        args:
            order_repository: instance of OrderRepository
            jwt_service: instance of JWTService
        """
        self.order_repository = order_repository
        self.jwt_service = jwt_service
    
    def get_user_orders(self, id_token):
        """
        get orders for user by validating their jwt token
        
        args:
            id_token (str): cognito id token from authorization header
            
        returns:
            list: list of user's orders
            
        raises:
            ValueError: if token invalid or user not found
        """
        # validate jwt and extract user info
        try:
            user_info = self.jwt_service.extract_user_info(id_token)
            cognito_sub = user_info['sub']
        except ValueError as e:
            raise ValueError(f"invalid token: {str(e)}")
        
        # find user by cognito sub
        user = self.order_repository.find_user_by_cognito_sub(cognito_sub)
        if not user:
            raise ValueError("user not found in system")
        
        user_id = user['PK']  # extract user_id
        
        # get orders for this user
        orders = self.order_repository.get_orders_by_user_id(user_id)
        
        return orders 