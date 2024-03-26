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

import com.opentext.app.entity.Review;
import org.springframework.jdbc.core.RowMapper;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.UUID;

public class ReviewMapper implements RowMapper<Review> {
    public Review mapRow(ResultSet rs, int rowNum) throws SQLException {
        Review Review = new Review();
        Review.setId(UUID.fromString(rs.getString("id")));
        Review.setProduct(UUID.fromString(rs.getString("product_id")));
        Review.setUsername(rs.getString("username"));
        Review.setReviewDate(rs.getDate("review_date"));
        Review.setComment(rs.getString(("comment")));
        Review.setRating(rs.getInt("rating"));
        Review.setVisible(rs.getBoolean("visible"));
        return Review;
    }
}
