
# This method only retrieve github positives entries
def filter_person_with_github(data):
    """
    Filters JSON-LD data to return entries that:
    - Have an "@type" containing "schema.org/Person".
    - Have an "@id" that includes "github.com".

    Args:
        data: The JSON-LD data (dict or list).

    Returns:
        A list of matching entries.
    """

    def is_person(entry):
        types = entry.get('@type', [])
        # Ensure types is a list for consistency.
        if not isinstance(types, list):
            types = [types]
        return any("schema.org/Person" in t for t in types)

    def has_github_id(entry):
        return "github.com" in entry.get('@id', "")

    result = []

    # If data contains a graph list or is already a list.
    if isinstance(data, dict):
        if '@graph' in data and isinstance(data['@graph'], list):
            entries = data['@graph']
        else:
            entries = [data]
    elif isinstance(data, list):
        entries = data
    else:
        entries = []

    for entry in entries:
        if isinstance(entry, dict) and is_person(entry) and has_github_id(entry):
            result.append(entry)

    return result