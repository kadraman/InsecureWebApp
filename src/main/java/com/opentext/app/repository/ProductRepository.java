/*
        FortifyDemoApp - an insecure web application.

        Copyright (C) Copyright 2024 OpenText Corp.

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

package com.opentext.app.repository;

import com.opentext.app.entity.Product;
import com.opentext.app.entity.Review;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public class ProductRepository {

    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public ProductRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<Product> findAll() {
        String sqlQuery = "select * from products";
        return jdbcTemplate.query(sqlQuery, new ProductMapper());
    }

    public int count() {
        String sqlQuery = "select count(*) from products";
        return jdbcTemplate.queryForObject(sqlQuery, Integer.class);
    }

    public List<Product> findByName(String keywords) {
        String query = keywords.toLowerCase();
        String sqlQuery = "SELECT * FROM " + getProductTableName() +
                " WHERE lower(name) LIKE '%" + query + "%' " +
                " OR lower(summary) LIKE '%" + query + "%'" +
                " OR lower(description) LIKE '%" + query + "%'";
        return jdbcTemplate.query(sqlQuery, new ProductMapper());
    }

    public List<Product> findById(UUID id) {
        String query = id.toString().toLowerCase();
        String sqlQuery = "SELECT * FROM " + getProductTableName() +
                " WHERE lower(id) LIKE '%" + query + "%'";
        return jdbcTemplate.query(sqlQuery, new ProductMapper());
    }

    public List<Review> reviewsByProductId(UUID id) {
        String query = id.toString().toLowerCase();
        String sqlQuery = "SELECT * FROM " + getReviewTableName() +
                " WHERE lower(product_id) LIKE '%" + query + "%'";
        return jdbcTemplate.query(sqlQuery, new ReviewMapper());
    }
    String getProductTableName() {
        return Product.TABLE_NAME;
    }
    String getReviewTableName() {
        return Review.TABLE_NAME;
    }

}
