def get_displacement_signal(
    zero_crossings: np.ndarray, time_signal: np.ndarray
) -> tuple[np.ndarray, int]:
    """
    Calculate the displacement signal based on the zero crossings and time signal.

    Args:
        zero_crossings (np.ndarray): An array of zero crossings.
        time_signal (np.ndarray): An array of time values corresponding to the raw signal of interest.

    Returns:
        tuple[np.ndarray, int]: A tuple containing the displacement signal corresponding to the signal of interest and the number of rotations.

    Note:
        This code is written for a Once Per Revolution (OPR) tacho signal. See getrpm_BCG for a Multiple
        Pulse per Revolution (MPR) tacho signal.
    """
    num_rotations = len(zero_crossings) - 1
    ones_array = np.ones(len(zero_crossings))
    ones_array[0] = 0  # cumulative displacement is zero at the beginning
    cumulative_displacement = np.cumsum(ones_array * np.pi * 2)  # Radians

    displacement_signal = np.interp(
        time_signal, zero_crossings, cumulative_displacement
    )

    return displacement_signal, num_rotations

def order_tracking(
    num_shaft_rot: int,
    disp_signal: np.ndarray,
    signal: np.ndarray,
    num_added_interp_points: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform order tracking on a signal of interest.

    Args:
        num_shaft_rot (int): Total number of shaft rotations corresponding to the signal of interest.
        disp_signal (np.ndarray): Displacement signal obtained from tachometer speed signal. Use BGC tachometer speed signal if applicable.
        signal (np.ndarray): Signal of interest. Signal you want to order track
        num_added_interp_points (int): Number of interpolated points per shaft revolution.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing the signal orders and the order tracked signal.

    Raises:
        None

    Examples:
        >>> num_shaft_rot = 10
        >>> disp_signal = np.array([0.1, 0.2, 0.3, 0.4])
        >>> signal = np.array([1, 2, 3, 4])
        >>> num_added_interp_points = 5
        >>> order_tracking(num_shaft_rot, disp_signal, signal, num_added_interp_points)
        (array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.]), array([1., 2., 3., 4., 1., 2., 3., 4., 1., 2., 3.]))
    Note:
        Note that if you would like to take the FFT of the order tracked signal you need to account for the updated sampling frequency corresponding to the order tracked signal. Thus can use Fs = 1/(signal_orders[1] - signal_orders[0])
    """
    points_per_rot = int(
        (num_added_interp_points + len(disp_signal) / num_shaft_rot) * num_shaft_rot
    )

    signal_orders = np.linspace(0, num_shaft_rot, points_per_rot)
    signal_OT = np.interp(signal_orders, disp_signal / (2 * np.pi), signal)

    return signal_orders, signal_OT

def inverse_order_tracking(
    # num_shaft_rot: int,
    disp_signal: np.ndarray,
    signal_orders: np.ndarray,
    order_tracked_signal: np.ndarray
) -> np.ndarray:
    """
    Convert an order tracked signal back to the time domain.

    Args:
        # num_shaft_rot (int): Total number of shaft rotations corresponding to the signal of interest.
        disp_signal (np.ndarray): Displacement signal obtained from tachometer speed signal. Use BGC tachometer speed signal if applicable.
        signal_orders (np.ndarray): Signal orders obtained from order tracking.
        order_tracked_signal (np.ndarray): Order tracked signal.

    Returns:
        np.ndarray: The signal converted back to the time domain.

    Raises:
        None

    Examples:
        >>> num_shaft_rot = 10
        >>> disp_signal = np.array([0.1, 0.2, 0.3, 0.4])
        >>> signal_orders = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])
        >>> order_tracked_signal = np.array([1., 2., 3., 4., 1., 2., 3., 4., 1., 2., 3.])
        >>> inverse_order_tracking(num_shaft_rot, disp_signal, signal_orders, order_tracked_signal)
        array([1., 2., 3., 4.])
    """
    # Normalize displacement signal to the range of signal orders
    normalized_disp_signal = disp_signal / (2 * np.pi)
    
    # Interpolate the order tracked signal back to the time domain
    time_domain_signal = np.interp(normalized_disp_signal, signal_orders, order_tracked_signal)
    
    return time_domain_signal