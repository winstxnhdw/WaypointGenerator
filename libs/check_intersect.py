import matplotlib.pyplot as plt

def on_segment(p, q, r):

    if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
        return True

    else:
        return False

def orientation(p, q, r):

    val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))

    if val == 0:
        return 0

    elif val > 0:
        return 1

    else:
        return -1

def gradient(x1, y1, x2, y2):

    m = (y2 - y1)/(x2 - x1)
    return m

def intersects(seg1, seg2):

    p1, q1 = seg1
    p2, q2 = seg2

    if seg1[-1] == seg2[0]:
        try:
            m1 = gradient(p1[0], p1[1], q1[0], q1[1])

        except ZeroDivisionError:
            return True

        m2 = gradient(p2[0], p2[1], q2[0], q2[1])

        if m1 == m2:
            return True
        
        else:
            return False

    else:
        pass

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    elif o1 == 0 and on_segment(p1, q1, p2): 
        return True

    elif o2 == 0 and on_segment(p1, q1, q2): 
        return True

    elif o3 == 0 and on_segment(p2, q2, p1): 
        return True

    elif o4 == 0 and on_segment(p2, q2, q1): 
        return True

    else:
        return False

def main():

    segment_one = ((53.43, -40.76), (33.53, -64.57))
    segment_two = ((40.91, -80.48), (17.83, -52.31))
    print(intersects(segment_one, segment_two))

    x1 = [segment_one[0][0]]
    y1 = [segment_one[0][1]]
    x1.append(segment_one[1][0])
    y1.append(segment_one[1][1])

    x2 = [segment_two[0][0]]
    y2 = [segment_two[0][1]]
    x2.append(segment_two[1][0])
    y2.append(segment_two[1][1])

    plt.figure()
    ax = plt.axes()
    ax.plot(x1, y1, '-o')
    ax.plot(x2, y2, '-o')
    plt.show()

if __name__ == '__main__':
    main()
