BEGIN TRANSACTION;
INSERT INTO `users` (`username`, `secret`) VALUES
    ('charles', '54f29855de99593f9292347a747768d6'),
    ('steve',    '49976a6cc84bd1231af3e121dc493ff7');
COMMIT;
