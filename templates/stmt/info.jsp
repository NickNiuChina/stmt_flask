<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>档案查询</title>

<%@ include file="/WEB-INF/pages/css_template.jsp"%>
</head>

<body>
	<nav class="navbar navbar-inverse navbar-fixed-top">
		<div class="container-fluid">
			<div class="navbar-header">
				<button type="button" class="navbar-toggle collapsed"
					data-toggle="collapse" data-target="#navbar" aria-expanded="false"
					aria-controls="navbar">
					<span class="sr-only">学生管理系统</span> <span class="icon-bar"></span>
					<span class="icon-bar"></span> <span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="${pageContext.request.contextPath}/mainUrl">学生管理系统</a>
			</div>
			<div id="navbar" class="navbar-collapse collapse">
				<!-- 导航条菜单 -->
				<%@ include file="/WEB-INF/pages/header_nav_template.jsp"%>

			</div>
		</div>
	</nav>

	<div class="container-fluid">
		<div class="row">
			<div class="col-sm-3 col-md-2 sidebar">

				<!-- 侧边栏 -->
				<jsp:include page="/WEB-INF/pages/side_nav_template.jsp">
					<jsp:param value="active" name="3" />
				</jsp:include>

			</div>
			<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
				<h1 class="page-header">${student.getDescription() }</h1>
				<form action="${pageContext.request.contextPath}/updateInfo	">
					<div>
						<div class="panel panel-default">
							<!-- Default panel contents -->
							<div class="panel-heading">个性签名</div>
							<div class="panel-body">
								<textarea class="form-control" name="description" rows="3">${student.getDescription()}</textarea>
							</div>
	
							<!-- List group -->
							<ul class="list-group">

								<li class="list-group-item"><span
									class="label label-primary">学&#12288号</span>
									${student.getStudentNo() }</li>

								<li class="list-group-item"><span
									class="label label-primary">姓&#12288名</span>
									${student.getStudentName() }</li>

								<li class="list-group-item"><span
									class="label label-primary">身份证</span> ${student.getIdCard() }</li>

								<li class="list-group-item"><span
									class="label label-primary">性别</span>
									
								
									<c:choose>
										<c:when test="${student.getGender() == 1}">
		                                                                                               男
		                                        </c:when>
	
										<c:otherwise>
		                                                                                               女
		                                </c:otherwise>
									</c:choose>	
									</li>


								<li class="list-group-item"><span
									class="label label-primary">年&#12288龄</span> ${student.age }</li>

								<li class="list-group-item"><span
									class="label label-primary">入学年份</span> ${student.year }</li>

							</ul>
						</div>

						<div>
							<button class="bth btn-primary" style="float: right;"
								type="submit">更新</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	</div>
</body>
</html>