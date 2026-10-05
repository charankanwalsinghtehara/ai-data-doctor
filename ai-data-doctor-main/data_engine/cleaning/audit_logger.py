def create_audit_log():
    """
    Create an empty cleaning audit log.
    """

    return []


def add_audit_entry(
    audit_log,
    action,
    details
):
    """
    Add one cleaning action to the audit log.
    """

    entry = {
        "action": action,
        "details": details
    }

    audit_log.append(entry)


def get_audit_log(audit_log):
    """
    Return the complete audit history.
    """

    return audit_log