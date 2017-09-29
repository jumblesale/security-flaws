from security_flaws.user import User


class Note:
    def __init__(self, from_user: User, to_user: User, note):
        self.from_user = from_user
        self.to_user = to_user
        self.note = note
        self.id = None

    def __str__(self):
        return "{}|{}|{}".format(
            self.from_user.username, self.to_user.username, self.note
        )


def create_note(from_user: User, to_user: User, note_text: str) -> Note:
    """
    create a Note object
    :param from_user: who to send the note to
    :param to_user: who the note is from
    :param note_text: the text of the note
    :return: a User object
    """
    return Note(from_user, to_user, note_text)
