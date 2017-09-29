BEGIN TRANSACTION;
INSERT INTO `users` (`username`, `secret`) VALUES
    ('charles', '98998807691dea19c41bea33cf86f360'),
    ('steve',    '49976a6cc84bd1231af3e121dc493ff7');
INSERT INTO `notes` (`from_user_id`, `from_username`, `to_user_id`, `note`) VALUES
    (2, 'steve', 1, 'hello charles!'),
    (2, 'steve', 1, 'how are you?');
COMMIT;
