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

package com.opentext.app.entity;

import java.util.Date;
import java.util.Objects;
import java.util.UUID;

public class Review  {

    public static final String TABLE_NAME = "reviews";

    private UUID Id;
    private UUID Product;
    private String Username;
    private Date ReviewDate;
    private String Comment;
    private int Rating;
    private Boolean Visible;

    public UUID getId() {
        return Id;
    }

    public void setId(UUID id) {
        this.Id = id;
    }

    public UUID getProduct() {
        return Product;
    }

    public void setProduct(UUID product) {
        this.Product = product;
    }

    public String getUsername() {
        return Username;
    }

    public void setUsername(String username) {
        this.Username = username;
    }

    public Date getReviewDate() {
        return ReviewDate;
    }

    public void setReviewDate(Date reviewDate) {
        this.ReviewDate = reviewDate;
    }

    public String getComment() {
        return Comment;
    }

    public void setComment(String comment) {
        this.Comment = comment;
    }

    public int getRating() {
        return Rating;
    }

    public void setRating(int rating) {
        this.Rating = rating;
    }

    public Boolean getVisible() {
        return Visible;
    }

    public void setVisible(Boolean visible) {
        this.Visible = visible;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Review review = (Review) o;
        return Rating == review.Rating && Objects.equals(Id, review.Id) && Objects.equals(Product, review.Product) && Objects.equals(Username, review.Username) && Objects.equals(ReviewDate, review.ReviewDate) && Objects.equals(Comment, review.Comment) && Objects.equals(Visible, review.Visible);
    }

    @Override
    public int hashCode() {
        return Objects.hash(Id, Product, Username, ReviewDate, Comment, Rating, Visible);
    }

    @Override
    public String toString() {
        return "Review{" +
                "Id=" + Id +
                ", Product=" + Product +
                ", Username=" + Username +
                ", ReviewDate=" + ReviewDate +
                ", Comment=" + Comment +
                ", Rating=" + Rating +
                '}';
    }
}
