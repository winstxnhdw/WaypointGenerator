import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main(args):
    
    mode = input("Point or Angle mode (p/a): ")

    if args.xradius and args.yradius:
        if mode == "p":
            point_mode(args.xradius, args.yradius)

        elif mode == "a":
            angle_mode(args.xradius, args.yradius)

        else:
            print("Invalid input.")
            main(args)
    
    else:
        if mode == "p":
            point_mode()

        elif mode == "a":
            angle_mode()
            
        else:
            print("Invalid input.")
            main(args)

def point_mode(a=1.0, b=1.0):

    try:
        if a != b:
            points = int(input("Number of points: "))

            print("\na: {}\nb: {}\nPoints: {}".format(a, b, points))

        else:
            r = float(input("Radius (m): "))
            points = int(input("Number of points: "))
            a = r
            b = r

            print("\nRadius: ", r, "\nPoints: ", points)

    except ValueError:
        print("Invalid input.")
        point_mode()

    theta = 0

    X = []
    Y = []

    theta = np.linspace(0, 2*np.pi, points)
    X = a * np.cos(theta)
    Y = b * np.sin(theta)

    axis = {'X-axis': X, 'Y-axis': Y}
    df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
    df.to_csv("waypoints.csv", index = False)
    plot_waypoints(df)

def angle_mode(a=1.0, b=1.0):

    try:
        if a != b:
            degrees = float(input("Angle in degrees: "))

            print("\na: {}\nb: {}\nAngle: {}".format(a, b, degrees))

        else:
            r = float(input("Radius (m): "))
            degrees = float(input("Angle in degrees: "))
            a = r
            b = r

            print("\nRadius: ", r, "\nAngle: ", degrees)
    
    except ValueError:
        print("Invalid input.")
        angle_mode()

    angle = np.radians(degrees)
    theta = 0

    X = []
    Y = []
    runs = int(2*np.pi/angle)

    for _ in np.arange(0, 2*np.pi, angle):
        x = a * np.cos(theta)
        y = b * np.sin(theta)
        theta = theta + angle
        X.append(x)
        Y.append(y)

    X.append(X[0])
    Y.append(Y[0])

    print("\n This program has looped ", runs, " times.")

    axis = {'X-axis': X, 'Y-axis': Y}
    df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
    df.to_csv("waypoints.csv", index = False)
    plot_waypoints(df)

def plot_waypoints(df):

    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal', adjustable='box')

    x = df['X-axis']
    y = df['Y-axis']
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    ax.plot(x, y)
    plt.show()

def parse_args():

    parser = argparse.ArgumentParser(description='Generate a ellipse')
    parser.add_argument('-a', '--xradius', type=float, metavar='', help='Radius of an ellipse on the x-axis')
    parser.add_argument('-b', '--yradius', type=float, metavar='', help='Radius of an ellipse on the y-axis')
    return parser.parse_known_args()
    
if __name__ == "__main__":
    args, _ = parse_args()
    main(args)