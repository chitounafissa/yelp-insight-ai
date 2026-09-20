-- Petit jeu de données fictif utilisé uniquement par la CI (GitHub Actions),
-- qui n'a pas accès au vrai dataset Yelp. Respecte les mêmes règles de qualité
-- que les données réelles (ville, notes 1-5, pas d'avis orphelin).

INSERT INTO business (business_id, name, city, state, stars, review_count, categories) VALUES
    ('biz_1', 'Test Sushi House', 'Philadelphia', 'PA', 4.5, 120, 'Restaurants, Sushi'),
    ('biz_2', 'Test Brunch Cafe', 'Philadelphia', 'PA', 4.0, 80, 'Restaurants, Breakfast'),
    ('biz_3', 'Test Pizza Place', 'Philadelphia', 'PA', 3.5, 200, 'Restaurants, Pizza');

INSERT INTO review (review_id, business_id, user_id, stars, text, review_date, useful, funny, cool) VALUES
    ('rev_1', 'biz_1', 'user_1', 5, 'Amazing sushi, fresh and creative.', '2023-01-15', 3, 0, 1),
    ('rev_2', 'biz_1', 'user_2', 4, 'Great service, a bit pricey.', '2023-02-10', 1, 0, 0),
    ('rev_3', 'biz_2', 'user_3', 4, 'Best brunch in town.', '2023-03-05', 2, 1, 0),
    ('rev_4', 'biz_2', 'user_4', 3, 'Good but crowded on weekends.', '2023-03-20', 0, 0, 0),
    ('rev_5', 'biz_3', 'user_5', 3, 'Decent pizza, nothing special.', '2023-04-01', 1, 0, 0);
