from core.exceptions import CustomException


class KakaoIpMismatchedException(CustomException):
    code = 401
    error_code = "USER__KAKAO_IP_MISMATCHED"
    message = "kakao registered ip and caller ip are mismatched"


class KakaoAccessTokenNotExistException(CustomException):
    code = 404
    error_code = "USER__KAKAO_ACCESS_TOKEN_NOT_EXIST"
    message = "kakao access token does not exist"


class KakaoServerTemporaryErrorException(CustomException):
    code = 500
    error_code = "USER__KAKAO_SERVER_TEMPORARY_ERROR"
    message = "kakao server temporary error occurred"


class KakaoUserIdNotRegisteredException(CustomException):
    code = 400
    error_code = "USER__KAKAO_USER_ID_NOT_REGISTERED"
    message = "kakao user id is not registered"


class GPNotFoundException(CustomException):
    code = 400
    error_code = "GP__NOT_FOUND"
    message = "gp was not found"


class AuthorizationMismatchedException(CustomException):
    code = 401
    error_code = 'USER__AUTHORIZATION_MISMATCHED'
    message = 'authorization is mismatched'
