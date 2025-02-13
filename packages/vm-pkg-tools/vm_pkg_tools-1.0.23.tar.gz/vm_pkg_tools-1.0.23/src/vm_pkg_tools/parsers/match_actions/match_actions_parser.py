import logging
from vm_pkg_tools.parsers.match_actions.points_parser import parse_point
from vm_pkg_tools.parsers.match_actions.set_parser import create_set_details
from vm_pkg_tools.utils.parser_utils import find_set_number


def parse_match_actions(content, lineups):
    """
    Parses match actions for each set, assigning:
    - set_id via enumerate(...)
    - point_id resetting to 1 for each set
    - action_id (1..N) in parse_point
    """

    lines = content.splitlines()

    # Identify lines that represent points (*p or ap)
    points_lines = [line.strip() for line in lines if line.startswith(("*p", "ap"))]
    logging.debug(f"Extracted {len(points_lines)} points lines: {points_lines}")

    # Identify set markers (**... set...)
    set_markers = [
        line.strip() for line in lines if line.startswith("**") and "set" in line
    ]

    if not set_markers:
        logging.warning("No set markers found in content.")
        return []

    sets = []
    for idx, set_marker in enumerate(set_markers, start=1):
        logging.debug(f"Processing set {idx}: {set_marker}")

        # Local point counter for each set
        point_counter = 1
        set_points = []

        for point_line in points_lines:
            set_number = find_set_number(point_line)
            if set_number == idx:
                point_idx = lines.index(point_line)

                # Identify next point or None if it's the last
                current_index_in_points = points_lines.index(point_line)
                next_point = (
                    points_lines[current_index_in_points + 1]
                    if points_lines.index(point_line) + 1 < len(points_lines)
                    else None
                )

                # Parse this point
                parsed_point = parse_point(
                    line=point_line,
                    content=content,
                    point_idx=point_idx,
                    next_point=next_point,
                )
                if parsed_point:
                    # Assign local point ID
                    parsed_point["point_id"] = point_counter
                    point_counter += 1

                    set_points.append(parsed_point)

        logging.debug(f"Points extracted for set {idx}: {set_points}")

        if not set_points:
            logging.warning(f"No points found for set {idx}.")

        # Create set details (dict) and attach a set_id
        set_details = create_set_details(idx, set_points, lineups)
        set_details["set_id"] = idx

        sets.append(set_details)

    return sets
