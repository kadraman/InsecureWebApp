<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>

<head>
	<meta charset="utf-8"/>
	<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>Fortify Demo App</title>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/bootstrap.min.css"/>">
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/fontawesome.all.css"/>"/>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/icomoon/style.css"/>"/>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/app.css"/>">
</head>

<body>

	<div id="app" class="d-flex flex-column min-vh-100 site-wrap">

		<jsp:include page="includes/header.jsp"></jsp:include>

		<!-- content -->
		<div class="site-section">
			<div class="container h-100">

				<div class="row align-items-center">
					<c:if test="${param.logout}" >
						<div class="auto-dismiss mx-auto">
							<div class="alert alert-info alert-dismissible'}" role="alert">
								<span>You have been logged out. Please re-login.</span>
								<button type="button" class="close" data-dismiss="alert" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>
						</div>
					</c:if>
				</div>

				<div class="row align-items-center">
					<img src="/img/login_logo.png" class="rounded mx-auto d-block" style="padding-top:20px;" alt="IWA Pharmacy Direct">
				</div>

				<div class="row justify-content-center align-items-center">

					<form name="f" action="/perform_login" method="post" class="form-login">
						<h1 class="h3 mb-3 font-weight-normal">Enter your details</h1>

						<div class="form-group">
							<input type="text" id="username" name="username" class="form-control"
								   autofocus="autofocus" placeholder="Username">
						</div>
						<div class="form-group mb-0">
							<input type="password" id="password" name="password" class="form-control" autocomplete="off"
								   placeholder="Password">
						</div>

						<c:if test="${param.error}" >
							<div class="pb-2">
								<div class="text-danger">
									<strong>
										Your login attempt was not successful, try again. Cause:&nbsp;
										${sessionScope["SPRING_SECURITY_LAST_EXCEPTION"].message}
									</strong>
								</div>
							</div>
						</c:if>

						<button class="btn btn-lg btn-primary btn-block" name="login-submit" id="login-submit" type="submit">Login</button>
					</form>

				</div>

			</div>

		</div>

		<jsp:include page="includes/footer.jsp"></jsp:include>

		<script type="text/javascript" src="<c:url value="/js/lib/jquery.min.js"/>"></script>
		<script type="text/javascript" src="<c:url value="/js/lib/bootstrap.bundle.min.js"/>"></script>
		<script type="text/javascript" src="<c:url value="/js/SubscribeNewsletter.js"/>"></script>
		<script type="text/javascript" src="<c:url value="/js/app.js"/>"></script>

		<script type="text/javascript">
			(function ($) {
				$(document).ready(function () {
					$('#subscribe-newsletter').SubscribeNewsletter();
				});
			})(jQuery);
		</script>

	</div>

</body>

</html>
