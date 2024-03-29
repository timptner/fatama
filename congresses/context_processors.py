from congresses.models import Congress


def congresses(request) -> dict:
    """Return the latest congress"""
    return {
        "the_congress": Congress.objects.order_by("-year").first(),
    }
