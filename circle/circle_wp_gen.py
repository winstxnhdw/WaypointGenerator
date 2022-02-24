import numpy as np
import pandas as pd

from argparse import ArgumentParser
from matplotlib import pyplot as plt

def point_mode(a=1.0, b=1.0):

    try:
        if a != b:
            points = int(input("Number of points: "))

            print(f"\na: {a}\nb: {b}\nPoints: {points}")

        else:
            r = float(input("Radius (m): "))
            points = int(input("Number of points: "))
            a = r
            b = r

            print(f"\nRadius: {r}\nPoints: {points}")

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
    plot_waypoints(X, Y)

def angle_mode(a=1.0, b=1.0):

    try:
        if a != b:
            degrees = float(input("Angle in degrees: "))

            print(f"\na: {a}\nb: {b}\nAngle: {degrees}")

        else:
            r = float(input("Radius (m): "))
            degrees = float(input("Angle in degrees: "))
            a = r
            b = r

            print(f"\nRadius: {r}\nAngle: {degrees}")
    
    except ValueError:
        print("Invalid input.")
        angle_mode()

    theta = np.arange(0, 2*np.pi, np.deg2rad(degrees))
    X = a * np.cos(theta)
    Y = b * np.sin(theta)
    X = np.concatenate((X, X[0]))
    Y = np.concatenate((Y, Y[0]))

    print(f"\nThis program has looped {int(2*np.pi/angle)} times.")

    axis = {'X-axis': X, 'Y-axis': Y}
    df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
    df.to_csv("waypoints.csv", index = False)
    plot_waypoints(X, Y)

def plot_waypoints(X, Y):

    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal', adjustable='box')

    ax.plot(X, Y)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

def main():
    
    args, _ = parse_args()
    mode = input("Point or Angle mode (p/a): ")

    if args.xradius and args.yradius:
        if mode == "p":
            point_mode(args.xradius, args.yradius)

        elif mode == "a":
            angle_mode(args.xradius, args.yradius)

        else:
            print("Invalid input.")
            main()
    
    else:
        if mode == "p":
            point_mode()

        elif mode == "a":
            angle_mode()
            
        else:
            print("Invalid input.")
            main()

def parse_args():

    parser = ArgumentParser(description='Generate a ellipse')
    parser.add_argument('-a', '--xradius', type=float, metavar='', help='Radius of an ellipse on the x-axis')
    parser.add_argument('-b', '--yradius', type=float, metavar='', help='Radius of an ellipse on the y-axis')

    return parser.parse_known_args()
    
if __name__ == "__main__":
    main()