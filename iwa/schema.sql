-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  phone TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  country TEXT,
  role TEXT,
  enabled BOOLEAN DEFAULT 1 NOT NULL,
  otp_enabled BOOLEAN DEFAULT 0 NOT NULL,
  otp_secret TEXT
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL,
  name TEXT NOT NULL,
  summary CLOB,
  description CLOB,
  image TEXT,
  price FLOAT NOT NULL,
  on_sale BOOLEAN DEFAULT 0 NOT NULL,
  sale_price FLOAT DEFAULT 0.0 NOT NULL,
  in_stock BOOLEAN DEFAULT 1 NOT NULL,
  time_to_stock INTEGER DEFAULT 1 NOT NULL,
  rating INTEGER DEFAULT 1 NOT NULL,
  available BOOLEAN DEFAULT 1 NOT NULL
);

CREATE TABLE reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  review_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comment CLOB,
  rating INTEGER DEFAULT 1 NOT NULL,
  visible BOOLEAN DEFAULT 1 NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Sample data

INSERT INTO users (id, username, password, first_name, last_name, email, phone, address, city, state, zip, country, date_created, role, enabled)
VALUES (1, 'admin@localhost.com', 'pbkdf2:sha256:600000$rvTTezuLMV6UMiNg$662c8f8a9089cb19de8136351c368ae7bf47ffd56a46276b66f3935d15756db2',
        'Admin', 'User', 'admin@localhost.com', '+44808123456', '', '', '', '', 'United Kingdom', CURRENT_TIMESTAMP, 'ROLE_ADMIN', 1);
INSERT INTO users (id, username, password, first_name, last_name, email, phone, address, city, state, zip, country, date_created, role, enabled)
VALUES (2, 'user1@localhost.com', 'pbkdf2:sha256:600000$J4OXxAF9HPp7X9yd$60364d73a428573c0987bc051c00f5e50cd6ba8a5aff51f65e88052c86db86d2',
        'Sam', 'Shopper', 'user1@localhost.com', '+44808123456', '1 Somewhere Street', 'London', 'Greater London', 'SW1', 'United Kingdom', CURRENT_TIMESTAMP, 'ROLE_USER', 1);
INSERT INTO users (id, username, password, first_name, last_name, email, phone, address, city, state, zip, country, date_created, role, enabled, otp_enabled, otp_secret)
VALUES (3, 'user2@localhost.com', 'pbkdf2:sha256:600000$J4OXxAF9HPp7X9yd$60364d73a428573c0987bc051c00f5e50cd6ba8a5aff51f65e88052c86db86d2',
        'Sarah', 'Shopper', 'user2@localhost.com', '+44808123456', '1 Somewhere Street', 'London', 'Greater London', 'SW1', 'United Kingdom', CURRENT_TIMESTAMP, 'ROLE_USER', 1, 1, 'base32secret3232');
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (1, 'SWA234-A568-00010', 'Solodox 750', 4,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin pharetra enim erat, sed tempor mauris viverra in. Donec ante diam, rhoncus dapibus efficitur ut, sagittis a elit. Integer non ante felis. Curabitur nec lectus ut velit bibendum euismod. Nulla mattis convallis neque ac euismod. Ut vel mattis lorem, nec tempus nibh. Vivamus tincidunt enim a risus placerat viverra. Curabitur diam sapien, posuere dignissim accumsan sed, tempus sit amet diam. Aliquam tincidunt vitae quam non rutrum. Nunc id sollicitudin neque, at posuere metus. Sed interdum ex erat, et ornare purus bibendum id. Suspendisse sagittis est dui. Donec vestibulum elit at arcu feugiat porttitor.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin pharetra enim erat, sed tempor mauris viverra in. Donec ante diam, rhoncus dapibus efficitur ut, sagittis a elit. Integer non ante felis. Curabitur nec lectus ut velit bibendum euismod. Nulla mattis convallis neque ac euismod. Ut vel mattis lorem, nec tempus nibh. Vivamus tincidunt enim a risus placerat viverra. Curabitur diam sapien, posuere dignissim accumsan sed, tempus sit amet diam. Aliquam tincidunt vitae quam non rutrum. Nunc id sollicitudin neque, at posuere metus. Sed interdum ex erat, et ornare purus bibendum id. Suspendisse sagittis est dui. Donec vestibulum elit at arcu feugiat porttitor.',
        'generic-product-4.jpg',
        12.95, 1, 30, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, on_sale, sale_price, in_stock, time_to_stock, available)
VALUES (2, 'SWA534-F528-00115', 'Alphadex Plus', 5,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet quam eget neque vestibulum tincidunt vitae vitae augue. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer rhoncus varius sem non luctus. Etiam tincidunt et leo non tempus. Etiam imperdiet elit arcu, a fermentum arcu commodo vel. Fusce vel consequat erat. Curabitur non lacus velit. Donec dignissim velit et sollicitudin pulvinar.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet quam eget neque vestibulum tincidunt vitae vitae augue. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer rhoncus varius sem non luctus. Etiam tincidunt et leo non tempus. Etiam imperdiet elit arcu, a fermentum arcu commodo vel. Fusce vel consequat erat. Curabitur non lacus velit. Donec dignissim velit et sollicitudin pulvinar.',
        'generic-product-1.jpg',
        14.95, 1, 9.95, 1, 30, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (3, 'SWA179-G243-00101', 'Dontax', 3,
        'Aenean sit amet pulvinar mauris. Suspendisse eu ligula malesuada, condimentum tortor rutrum, rutrum dui. Sed vehicula augue sit amet placerat bibendum. Maecenas ac odio libero. Donec mi neque, convallis ut nulla quis, malesuada convallis velit. Aenean a augue blandit, viverra massa nec, laoreet quam. In lacinia eros quis lacus dictum pharetra.',
        'Aenean sit amet pulvinar mauris. Suspendisse eu ligula malesuada, condimentum tortor rutrum, rutrum dui. Sed vehicula augue sit amet placerat bibendum. Maecenas ac odio libero. Donec mi neque, convallis ut nulla quis, malesuada convallis velit. Aenean a augue blandit, viverra massa nec, laoreet quam. In lacinia eros quis lacus dictum pharetra.',
        'generic-product-2.jpg',
        8.50, 1, 30, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, on_sale, sale_price, in_stock, time_to_stock, available)
VALUES (4, 'SWA201-D342-00132', 'Tranix Life', 5,
        'Curabitur imperdiet lacus nec lacus feugiat varius. Integer hendrerit erat orci, eget varius urna varius ac. Nulla fringilla, felis eget cursus imperdiet, odio eros tincidunt est, non blandit enim ante nec magna. Suspendisse in justo maximus nisi molestie bibendum. Fusce consequat accumsan nulla, vel pharetra nulla consequat sit amet.',
        'Curabitur imperdiet lacus nec lacus feugiat varius. Integer hendrerit erat orci, eget varius urna varius ac. Nulla fringilla, felis eget cursus imperdiet, odio eros tincidunt est, non blandit enim ante nec magna. Suspendisse in justo maximus nisi molestie bibendum. Fusce consequat accumsan nulla, vel pharetra nulla consequat sit amet.',
        'generic-product-3.jpg',
        7.95, 1, 4.95, 1, 14, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (5, 'SWA312-F432-00134', 'Salex Two', 5,
        'In porta viverra condimentum. Morbi nibh magna, suscipit sit amet urna sed, euismod consectetur eros. Donec egestas, elit ut commodo fringilla, sem quam suscipit lectus, id tempus enim sem quis risus. Curabitur eleifend bibendum magna, vel iaculis elit varius et. Sed mollis dolor quis metus lacinia posuere. Phasellus odio mi, tempus quis dui et, consectetur iaculis odio. Quisque fringilla viverra eleifend. Cras dignissim euismod tortor, eget congue turpis fringilla sit amet. Aenean sed semper dolor, sed ultrices felis.',
        'In porta viverra condimentum. Morbi nibh magna, suscipit sit amet urna sed, euismod consectetur eros. Donec egestas, elit ut commodo fringilla, sem quam suscipit lectus, id tempus enim sem quis risus. Curabitur eleifend bibendum magna, vel iaculis elit varius et. Sed mollis dolor quis metus lacinia posuere. Phasellus odio mi, tempus quis dui et, consectetur iaculis odio. Quisque fringilla viverra eleifend. Cras dignissim euismod tortor, eget congue turpis fringilla sit amet. Aenean sed semper dolor, sed ultrices felis.',
        'generic-product-5.jpg',
        11.95, 0, 14, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, on_sale, sale_price, in_stock, time_to_stock, available)
VALUES (6, 'SWA654-F106-00412', 'Betala Lite', 5,
        'Sed bibendum metus vitae suscipit mattis. Mauris turpis purus, sodales a egestas vel, tincidunt ac ipsum. Donec in sapien et quam varius dignissim. Phasellus eros sem, facilisis quis vehicula sed, ornare eget odio. Nam tincidunt urna mauris, id tincidunt risus posuere ac. Integer vel est vel enim convallis blandit sed sed urna. Nam dapibus erat nunc, id euismod diam pulvinar id. Fusce a felis justo.',
        'Sed bibendum metus vitae suscipit mattis. Mauris turpis purus, sodales a egestas vel, tincidunt ac ipsum. Donec in sapien et quam varius dignissim. Phasellus eros sem, facilisis quis vehicula sed, ornare eget odio. Nam tincidunt urna mauris, id tincidunt risus posuere ac. Integer vel est vel enim convallis blandit sed sed urna. Nam dapibus erat nunc, id euismod diam pulvinar id. Fusce a felis justo.',
        'generic-product-4.jpg',
        11.95, 1, 9.95, 1, 30, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (7, 'SWA254-A971-00213', 'Stimlab Mitre', 5,
        'Phasellus malesuada pulvinar justo, ac eleifend magna lacinia eget. Proin vulputate nec odio at volutpat. Duis non suscipit arcu. Nam et arcu vehicula, sollicitudin eros non, scelerisque diam. Phasellus sagittis pretium tristique. Vestibulum sit amet lectus nisl. Aliquam aliquet dolor sit amet neque placerat, vel varius metus molestie. Fusce sed ipsum blandit, efficitur est vitae, scelerisque enim. Integer porttitor est et dictum blandit. Quisque gravida tempus orci nec finibus.',
        'Phasellus malesuada pulvinar justo, ac eleifend magna lacinia eget. Proin vulputate nec odio at volutpat. Duis non suscipit arcu. Nam et arcu vehicula, sollicitudin eros non, scelerisque diam. Phasellus sagittis pretium tristique. Vestibulum sit amet lectus nisl. Aliquam aliquet dolor sit amet neque placerat, vel varius metus molestie. Fusce sed ipsum blandit, efficitur est vitae, scelerisque enim. Integer porttitor est et dictum blandit. Quisque gravida tempus orci nec finibus.',
        'generic-product-6.jpg',
        12.95, 0, 7, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (8, 'SWA754-B418-00315', 'Alphadex Lite', 2,
        'Nam bibendum porta metus. Aliquam viverra pulvinar velit et condimentum. Pellentesque quis purus libero. Fusce hendrerit tortor sed nulla lobortis commodo. Donec ultrices mi et sollicitudin aliquam. Phasellus rhoncus commodo odio quis faucibus. Nullam interdum mi non egestas pellentesque. Duis nec porta leo, eu placerat tellus.',
        'Nam bibendum porta metus. Aliquam viverra pulvinar velit et condimentum. Pellentesque quis purus libero. Fusce hendrerit tortor sed nulla lobortis commodo. Donec ultrices mi et sollicitudin aliquam. Phasellus rhoncus commodo odio quis faucibus. Nullam interdum mi non egestas pellentesque. Duis nec porta leo, eu placerat tellus.',
        'generic-product-7.jpg', 9.95, 1, 30, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (9, 'SWA432-E901-00126', 'Villacore 2000', 1,
        'Aliquam erat volutpat. Ut gravida scelerisque purus a sagittis. Nullam pellentesque arcu sed risus dignissim scelerisque. Maecenas vel elit pretium, ultrices augue ac, interdum libero. Suspendisse potenti. In felis metus, mattis quis lorem congue, condimentum volutpat felis. Nullam mauris mi, bibendum in ultrices sed, blandit congue ipsum.',
        'Aliquam erat volutpat. Ut gravida scelerisque purus a sagittis. Nullam pellentesque arcu sed risus dignissim scelerisque. Maecenas vel elit pretium, ultrices augue ac, interdum libero. Suspendisse potenti. In felis metus, mattis quis lorem congue, condimentum volutpat felis. Nullam mauris mi, bibendum in ultrices sed, blandit congue ipsum.',
        'generic-product-8.jpg',
        19.95, 1, 30, 1);
INSERT INTO products (id, code, name, rating, summary, description, image, price, in_stock, time_to_stock, available)
VALUES (10, 'SWA723-A375-00412', 'Kanlab Blue', 5,
        'Proin eget nisl non sapien gravida pellentesque. Cras tincidunt tortor posuere, laoreet sapien nec, tincidunt nunc. Integer vehicula, erat ut pretium porta, velit leo dignissim odio, eu ultricies urna nulla a dui. Proin et dapibus turpis, et tincidunt augue. In mattis luctus elit, in vehicula erat pretium sed. Suspendisse ullamcorper mollis dolor eu tristique.',
        'Proin eget nisl non sapien gravida pellentesque. Cras tincidunt tortor posuere, laoreet sapien nec, tincidunt nunc. Integer vehicula, erat ut pretium porta, velit leo dignissim odio, eu ultricies urna nulla a dui. Proin et dapibus turpis, et tincidunt augue. In mattis luctus elit, in vehicula erat pretium sed. Suspendisse ullamcorper mollis dolor eu tristique.',
        'generic-product-9.jpg',
        9.95, 0, 7, 1);
INSERT INTO reviews (id, product_id, user_id, review_date, comment, rating, visible)
VALUES (1, 1, 2,
        CURRENT_TIMESTAMP, 'This is an example review of Solodox 750. It is very good.', 5, 1);
INSERT INTO reviews (id, product_id, user_id, review_date, comment, rating, visible)
VALUES (2, 2, 3,
        CURRENT_TIMESTAMP, 'Arrived on time and works well but the instructions are very limited and not explained well.', 4, 1);
INSERT INTO reviews (id, product_id, user_id, review_date, comment, rating, visible)
VALUES (3, 1, 2,
        CURRENT_TIMESTAMP, 'This is another review of Solodox 750. It does not work as described and not worth the money.', 3, 1);        