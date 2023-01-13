def timing_traffic_lights(traffic):
    """
    traffic - instance of the class Traffic. Consist of traffic number in each lane

    return green time at line left-righr, green time at line top-bottom
    """
    print(type(traffic))
    max_cycle_time = 120
    sum_traf_l_r = traffic.from_left + traffic.from_right
    sum_traf_t_b = traffic.from_top + traffic.from_bottom

    time_l_r = sum_traf_l_r * max_cycle_time // (sum_traf_l_r + sum_traf_t_b)

    if time_l_r < 15:
        time_l_r = 15
    time_t_b = max_cycle_time - time_l_r
    if time_t_b < 15:
        time_t_b = 15
    time_l_r = max_cycle_time - time_t_b
    return time_l_r, time_t_b
