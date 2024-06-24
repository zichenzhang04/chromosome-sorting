import pybedtools
from pybedtools import BedTool


def process_left(ChIA_Drop_old, left_anchor, right_anchor, region):
    left_anchor_chrom = left_anchor.split('\t')[0]
    left_anchor_start = int(left_anchor.split('\t')[1])
    left_anchor_end = int(left_anchor.split('\t')[2])
    right_anchor_end = int(right_anchor.split('\t')[2])

    print("Filter GEMs to only include those in the region")
    ChIA_Drop = ChIA_Drop_old.intersect(BedTool(region, from_string=True), wa=True, wb=True)

    print("Create BedTool object for the left anchor")
    left_anchor_bed = BedTool(left_anchor, from_string=True)

    print("Get the GEM IDs that intersect with the left anchor")
    intersecting_fragments = ChIA_Drop.intersect(left_anchor_bed, wa=True, wb=True)
    intersecting_gem_ids = set(fragment.fields[4] for fragment in intersecting_fragments)
    print("Filter ChIA_Drop to only include GEMs with intersecting IDs")
    ChIA_Drop = ChIA_Drop.filter(lambda x: x.fields[4] in intersecting_gem_ids)

    # print("Filter ChIA_Drop to only include GEMs with the correct chrom id")
    # ChIA_Drop = ChIA_Drop.filter(lambda x: x.chrom == left_anchor_chrom)

    print("Group GEM fragments by their GEM ID and get the min start and max end positions")
    grouped_gems = {}
    for fragment_interval in ChIA_Drop:
        fragment = fragment_interval.fields
        gem_id = fragment[4]
        gem_size = int(fragment[3])
        start = int(fragment[1])
        end = int(fragment[2])

        if gem_id not in grouped_gems.keys():
            grouped_gems[gem_id] = {
                'min_start': start,
                'max_end': end,
                'fragments': [fragment],
                'gem_size': gem_size
            }
        else:
            grouped_gems[gem_id]['min_start'] = min(grouped_gems[gem_id]['min_start'], start)
            grouped_gems[gem_id]['max_end'] = max(grouped_gems[gem_id]['max_end'], end)
            grouped_gems[gem_id]['fragments'].append(fragment)

    print("Add valid gems")
    valid_gems = []
    for gem_id, gem_info in grouped_gems.items():
        leftmost_fragment_start = gem_info['min_start']
        rightmost_fragment_end = gem_info['max_end']
        gem_size = gem_info['gem_size']
        gem_length = rightmost_fragment_end - leftmost_fragment_start

        if (
            leftmost_fragment_start >= left_anchor_start
            and leftmost_fragment_start <= left_anchor_end
            and rightmost_fragment_end <= right_anchor_end
            and len(gem_info['fragments']) == gem_size
        ):
            # Get all fragments of the valid GEM
            fragments = [
                pybedtools.create_interval_from_list(fragment)
                for fragment in gem_info['fragments']
            ]
            valid_gems.append((gem_id, fragments, gem_length))

    print("Sort the valid GEMs by their length")
    valid_gems.sort(key=lambda x: x[2])
    # print(valid_gems)
    return valid_gems


def process_both(ChIA_Drop_old, left_anchor, right_anchor, region):
    left_anchor_chrom = left_anchor.split('\t')[0]
    left_anchor_start = int(left_anchor.split('\t')[1])
    left_anchor_end = int(left_anchor.split('\t')[2])
    right_anchor_start = int(right_anchor.split('\t')[1])
    right_anchor_end = int(right_anchor.split('\t')[2])

    print("Filter GEMs to only include those in the region")
    ChIA_Drop = ChIA_Drop_old.intersect(BedTool(region, from_string=True), wa=True, wb=True)

    print("Filter ChIA_Drop to only include GEMs with the correct chrom id")
    ChIA_Drop = ChIA_Drop.filter(lambda x: x.chrom == left_anchor_chrom)

    print("Group GEM fragments by their GEM ID and get the min start and max end positions")
    grouped_gems = {}
    for fragment_interval in ChIA_Drop:
        fragment = fragment_interval.fields
        gem_id = fragment[4]
        gem_size = int(fragment[3])
        start = int(fragment[1])
        end = int(fragment[2])

        if gem_id not in grouped_gems.keys():
            grouped_gems[gem_id] = {
                'min_start': start,
                'max_end': end,
                'fragments': [fragment],
                'gem_size': gem_size
            }
        else:
            grouped_gems[gem_id]['min_start'] = min(grouped_gems[gem_id]['min_start'], start)
            grouped_gems[gem_id]['max_end'] = max(grouped_gems[gem_id]['max_end'], end)
            grouped_gems[gem_id]['fragments'].append(fragment)

    print("Add valid gems")
    valid_gems = []
    for gem_id, gem_info in grouped_gems.items():
        leftmost_fragment_start = gem_info['min_start']
        rightmost_fragment_end = gem_info['max_end']
        gem_size = gem_info['gem_size']
        gem_length = rightmost_fragment_end - leftmost_fragment_start

        if (
            leftmost_fragment_start <= left_anchor_end and
            leftmost_fragment_start >= left_anchor_start and
            rightmost_fragment_end <= right_anchor_end and
            rightmost_fragment_end >= right_anchor_start and
            len(gem_info['fragments']) == gem_size
        ):
            # Get all fragments of the valid GEM
            fragments = [
                pybedtools.create_interval_from_list(fragment)
                for fragment in gem_info['fragments']
            ]
            valid_gems.append((gem_id, fragments, gem_length))

    print("Sort the valid GEMs by their length")
    valid_gems.sort(key=lambda x: x[2])
    print(valid_gems)
    return valid_gems


def process_right(ChIA_Drop_old, left_anchor, right_anchor, region):
    left_anchor_chrom = left_anchor.split('\t')[0]
    left_anchor_start = int(left_anchor.split('\t')[1])
    left_anchor_end = int(left_anchor.split('\t')[2])
    right_anchor_end = int(right_anchor.split('\t')[2])

    print("Filter GEMs to only include those in the region")
    ChIA_Drop = ChIA_Drop_old.intersect(BedTool(region, from_string=True), wa=True, wb=True)

    print("Create BedTool object for the right anchor")
    right_anchor_bed = BedTool(right_anchor, from_string=True)

    print("Get the GEM IDs that intersect with the right anchor")
    intersecting_fragments = ChIA_Drop.intersect(right_anchor_bed, wa=True, wb=True)
    intersecting_gem_ids = set(fragment.fields[4] for fragment in intersecting_fragments)
    print("Filter ChIA_Drop to only include GEMs with intersecting IDs")
    ChIA_Drop = ChIA_Drop.filter(lambda x: x.fields[4] in intersecting_gem_ids)

    print("Filter ChIA_Drop to only include GEMs with the correct chrom id")
    ChIA_Drop = ChIA_Drop.filter(lambda x: x.chrom == left_anchor_chrom)

    print("Group GEM fragments by their GEM ID and get the min start and max end positions")
    grouped_gems = {}
    for fragment_interval in ChIA_Drop:
        fragment = fragment_interval.fields
        gem_id = fragment[4]
        gem_size = int(fragment[3])
        start = int(fragment[1])
        end = int(fragment[2])

        if gem_id not in grouped_gems.keys():
            grouped_gems[gem_id] = {
                'min_start': start,
                'max_end': end,
                'fragments': [fragment],
                'gem_size': gem_size
            }
        else:
            grouped_gems[gem_id]['min_start'] = min(grouped_gems[gem_id]['min_start'], start)
            grouped_gems[gem_id]['max_end'] = max(grouped_gems[gem_id]['max_end'], end)
            grouped_gems[gem_id]['fragments'].append(fragment)

    print("Add valid gems")
    valid_gems = []
    for gem_id, gem_info in grouped_gems.items():
        leftmost_fragment_start = gem_info['min_start']
        rightmost_fragment_end = gem_info['max_end']
        gem_size = gem_info['gem_size']
        gem_length = rightmost_fragment_end - leftmost_fragment_start

        if (
            rightmost_fragment_end <= right_anchor_end
            and leftmost_fragment_start >= left_anchor_start
            and len(gem_info['fragments']) == gem_size
        ):
            # Get all fragments of the valid GEM
            fragments = [
                pybedtools.create_interval_from_list(fragment)
                for fragment in gem_info['fragments']
            ]
            valid_gems.append((gem_id, fragments, gem_length))

    print("Sort the valid GEMs by their length")
    valid_gems.sort(key=lambda x: x[2])
    print(valid_gems)
    return valid_gems


def process_middle(ChIA_Drop_old, left_anchor, right_anchor, region, middle_anchor):
    middle_anchor_chrom, positions = middle_anchor.split(':')
    middle_anchor_start, middle_anchor_end = positions.split('-')

    left_anchor_start = int(left_anchor.split('\t')[1])
    left_anchor_end = int(left_anchor.split('\t')[2])
    right_anchor_end = int(right_anchor.split('\t')[2])

    # Filter by range
    ChIA_Drop = ChIA_Drop_old.intersect(BedTool(region, from_string=True), wa=True, wb=True)

    # Create BedTool object for the middle anchor
    middle_anchor_bed = BedTool(
        f"{middle_anchor_chrom}\t{middle_anchor_start}\t{middle_anchor_end}",
        from_string=True
    )

    # Intersect ChIA_Drop with middle_anchor to get candidate GEMs
    candidate_gems = ChIA_Drop.intersect(middle_anchor_bed, wa=True, u=True)

    # Filter by chromosome
    candidate_gems = candidate_gems.filter(lambda x: x.chrom == middle_anchor_chrom)

    # Get unique GEM IDs from candidate GEMs
    candidate_gem_ids = set(fragment[4] for fragment in candidate_gems)

    # Filter ChIA_Drop to retain only GEMs with IDs in candidate_gem_ids
    valid_gems = []
    gem_fragments = {}
    gem_lengths = {}

    for fragment in ChIA_Drop:
        gem_id = fragment[4]
        if gem_id in candidate_gem_ids:
            if gem_id not in gem_fragments:
                gem_fragments[gem_id] = []
            gem_fragments[gem_id].append(fragment)

            start = int(fragment[1])
            end = int(fragment[2])
            if gem_id in gem_lengths:
                gem_lengths[gem_id] = (min(gem_lengths[gem_id][0], start), max(gem_lengths[gem_id][1], end))
            else:
                gem_lengths[gem_id] = (start, end)

    # Further filter valid GEMs based on the leftmost fragment and right anchor
    for gem_id, fragments in gem_fragments.items():
        leftmost_fragment_start = int(fragments[0][1])
        leftmost_fragment_end = int(fragments[0][2])
        _, end = gem_lengths[gem_id]

        if leftmost_fragment_start >= left_anchor_start and end <= right_anchor_end:
            valid_gems.append((gem_id, fragments, end - leftmost_fragment_start))

    # Sort GEMs by their length
    valid_gems.sort(key=lambda x: x[2])

    print(valid_gems)

    return valid_gems


def process_only_middle(ChIA_Drop_old, middle_region):
    middle_anchor_chrom, positions = middle_region.split(':')
    middle_anchor_start, middle_anchor_end = positions.split('-')

    # Create BedTool object for the middle anchor
    middle_anchor_bed = BedTool(
        f"{middle_anchor_chrom}\t{middle_anchor_start}\t{middle_anchor_end}",
        from_string=True
    )

    # Intersect ChIA_Drop with middle_anchor to get candidate GEMs
    candidate_gems = ChIA_Drop_old.intersect(middle_anchor_bed, wa=True, u=True)

    # Filter by chromosome
    candidate_gems = candidate_gems.filter(lambda x: x.chrom == middle_anchor_chrom)

    # Get unique GEM IDs from candidate GEMs
    candidate_gem_ids = set(fragment[4] for fragment in candidate_gems)

    # Filter ChIA_Drop to retain only GEMs with IDs in candidate_gem_ids
    valid_gems = []
    gem_fragments = {}
    gem_lengths = {}

    for fragment in ChIA_Drop_old:
        gem_id = fragment[4]
        if gem_id in candidate_gem_ids:
            if gem_id not in gem_fragments:
                gem_fragments[gem_id] = []
            gem_fragments[gem_id].append(fragment)

            start = int(fragment[1])
            end = int(fragment[2])
            if gem_id in gem_lengths:
                gem_lengths[gem_id] = (min(gem_lengths[gem_id][0], start), max(gem_lengths[gem_id][1], end))
            else:
                gem_lengths[gem_id] = (start, end)

    # Further filter valid GEMs based on the leftmost fragment and right anchor
    for gem_id, fragments in gem_fragments.items():
        leftmost_fragment_start = int(fragments[0][1])
        leftmost_fragment_end = int(fragments[0][2])
        rightmost_fragment_start = int(fragments[-1][1])
        rightmost_fragment_end = int(fragments[-1][2])
        _, end = gem_lengths[gem_id]

        if (leftmost_fragment_start >= int(middle_anchor_start) and leftmost_fragment_end <= int(middle_anchor_end)) \
        or (rightmost_fragment_start >= int(middle_anchor_start) and rightmost_fragment_end <= int(middle_anchor_end)):
            valid_gems.append((gem_id, fragments, end - leftmost_fragment_start))

    # Sort GEMs by their length
    valid_gems.sort(key=lambda x: x[2])

    return valid_gems


def process_only_middle_1frag(ChIA_Drop_old, middle_region):
    middle_anchor_chrom, positions = middle_region.split(':')
    middle_anchor_start, middle_anchor_end = map(int, positions.split('-'))

    # Create BedTool object for the middle anchor
    middle_anchor_bed = BedTool(
        f"{middle_anchor_chrom}\t{middle_anchor_start}\t{middle_anchor_end}",
        from_string=True
    )

    # Intersect ChIA_Drop with middle_anchor to get candidate fragments
    candidate_frag = ChIA_Drop_old.intersect(middle_anchor_bed, wa=True, u=True)

    # Filter by chromosome
    candidate_frag = candidate_frag.filter(lambda x: x.chrom == middle_anchor_chrom)

    # Group fragments by GEM ID and calculate lengths
    gem_fragments = {}
    gem_lengths = {}

    for fragment in candidate_frag:
        gem_id = fragment[4]  # GEM ID
        start = int(fragment[1])
        end = int(fragment[2])

        if gem_id not in gem_fragments:
            gem_fragments[gem_id] = []
        gem_fragments[gem_id].append(fragment)

        if gem_id in gem_lengths:
            gem_lengths[gem_id] = (min(gem_lengths[gem_id][0], start), max(gem_lengths[gem_id][1], end))
        else:
            gem_lengths[gem_id] = (start, end)

    # Filter valid GEMs
    valid_gems = []
    for gem_id, fragments in gem_fragments.items():
        start, end = gem_lengths[gem_id]
        gem_length = end - start
        if start >= middle_anchor_start and end <= middle_anchor_end:
            valid_gems.append((gem_id, fragments, gem_length))

    # Sort GEMs by their length
    valid_gems.sort(key=lambda x: x[2])

    return valid_gems
