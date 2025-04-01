def compute_total_and_difference(total_given_date, total_given_date_prev):
    return {
        'total': total_given_date,
        'difference': (total_given_date or 0) - (total_given_date_prev or 0),
        'difference_percent': 100 * ((total_given_date or 0) / (total_given_date_prev or 1)) - 100
    }
