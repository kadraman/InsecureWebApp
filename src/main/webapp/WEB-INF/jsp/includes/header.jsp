<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>

<!-- header -->
<div class="site-navbar py-2">
    <div class="container">
        <div class="d-flex align-items-center justify-content-between">
            <div class="logo">
                <div class="site-logo">
                    <a class="navbar-brand js-logo-clone" href="/">
                        <img src="<c:url value="/img/logo.png"/>" alt="IWA Pharmacy Direct">
                    </a>
                </div>
            </div>
            <div class="main-nav d-none d-lg-block">
                <nav class="site-navigation text-right text-md-center" role="navigation">
                    <ul class="site-menu js-clone-nav d-none d-lg-block">
                        <li class="has-children">
                            <a href="/">Shop</a>
                            <ul class="dropdown">
                                <li class="has-children">
                                    <a href="/">Health &amp; wellbeing</a>
                                    <ul class="dropdown">
                                        <li><a href="#">First aid</a></li>
                                        <li><a href="#">Health conditions</a></li>
                                        <li><a href="#">Stop smoking</a></li>
                                    </ul>
                                </li>
                                <li class="has-children">
                                    <a href="/">Medicines &amp; treatments</a>
                                    <ul class="dropdown">
                                        <li><a href="#">Allergy &amp; hayfever</a></li>
                                        <li><a href="#">Children's medicines</a></li>
                                        <li><a href="#">Cough, cold &amp; flu</a></li>
                                        <li><a href="#">Pain relief</a></li>
                                    </ul>
                                </li>
                                <li class="has-children">
                                    <a href="/">Vitamins &amp; supplements</a>
                                    <ul class="dropdown">
                                        <li><a href="#">Everyday vitamins &amp; supplements</a></li>
                                        <li><a href="#">Children's vitamins &amp; supplements</a></li>
                                        <li><a href="#">Mens supplements</a></li>
                                        <li><a href="#">Womens supplements</a></li>
                                    </ul>
                                </li>
                                <li><a href="/">Weight management</a></li>
                                <li><a href="/">Toiletries</a></li>
                            </ul>
                        </li>
                        <li class="has-children">
                            <a href="">Prescriptions</a>
                            <ul class="dropdown">
                                <li>
                                    <a href="#">One-off prescriptions</a>
                                    <a href="#">Repeat prescriptions</a>
                                </li>
                            </ul>
                        </li>
                        <li class="has-children">
                            <a href="#">Services</a>
                            <ul class="dropdown">
                                <li>
                                    <a href="#">Flu vaccinations</a>
                                    <a href="#">Stop smoking</a>
                                    <a href="#">Travel vaccinations</a>
                                </li>
                            </ul>
                        </li>
                        <li>
                            <a href="#">Advice</a>
                        </li>
                    </ul>
                </nav>
            </div>

            <div class="site-top-icons">
                <ul>
                    <li>
                        <div class="has-children">
                            <sec:authorize access="isAnonymous()">
                                <a href="/login" class="icons-menu d-inline-block">
                                    <span class="icon-account_circle"></span>
                                    <span class="my-account-text">My Account</span>
                                </a>
                                <ul class="dropdown">
                                    <li>
                                        <a href="/login">
                                            <i class="fas fa-sign-in-alt fa-fw"></i> Login
                                        </a>
                                    </li>
                                </ul>
                            </sec:authorize>
                            <sec:authorize access="isAuthenticated()">
                                <a href="/user" class="icons-menu d-inline-block">
                                    <span class="icon-account_circle"></span>
                                    <span class="my-account-text"><sec:authentication property="name"/></span>
                                </a>
                                <ul class="dropdown">
                                    <li>
                                        <a th:href="/user"><i class="fas fa-home fa-fw"></i> Home </a>
                                    </li>
                                    <sec:authorize access="hasRole('ROLE_ADMIN')">
                                        <li>
                                            <a th:href="/admin"><i class="fas fa-tools fa-fw"></i> Site Administration </a>
                                        </li>
                                        <li sec:authorize="hasRole('ROLE_ADMIN')">
                                            <a th:href="/console" target="_blank"><i class="fas fa-database fa-fw"></i> Database Console</a>
                                        </li>
                                    </sec:authorize>
                                    <li>
                                        <a class="nav-link" href="/logout"><i class="fas fa-sign-out-alt fa-fw"></i> Logout </a>
                                    </li>
                                </ul>
                            </sec:authorize>
                        </div>
                    </li>
                    <li>
                        <a href=#" class="icons-btn d-inline-block bag">
                            <span class="icon-shopping-bag"></span>
                            <span id="shopping-cart-count" class="number">0</span>
                        </a>
                    </li>
                    <li>
                        <a href="#" class="site-menu-toggle js-menu-toggle ml-3 d-inline-block d-lg-none">
                            <span class="icon-menu"></span>
                        </a>
                    </li>
                </ul>
            </div>

        </div>
    </div>
</div>
