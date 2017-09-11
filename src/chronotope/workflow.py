from chronotope.model.facility import Facility


def persist_publication_state(node, info):
    """Chronotoper publication workflow specific transition callback for
    repoze.workflow.
    """
    to_state = info.transition[u'to_state']
    # publish facility related locations if facility gets published but
    # related locations are not published yet
    if to_state == 'published' and isinstance(node, Facility):
        for location in node.attrs['location']:
            if location.state != 'published':
                location.state = to_state
    node.state = to_state
    node()
