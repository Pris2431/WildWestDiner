from mail import send_mail


def test_send():
    message = \
        """Hello, this is the test email"""
    send_mail("PRISCILLALOI.23@ichat.sp.edu.sg", "Test Email", [message])
    # We cannot verify the receipt of the email, hence we are just checking if any errors.
