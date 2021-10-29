'''
    Computing the height of Puaka James Height with rudimentary inclinometer
'''

# - Imports

import geopy.distance
import math
import csv
from typing import Dict
from jmath.uncertainties import mean

# - Classes

class Observation:
    '''
        An observation of angle of inclination

        Parameters
        ----------

        latitude
            The latitude of the observation
        longitude
            The longitude of the observation
        angle
            The angle (in radians) of inclination observed
    '''
    def __init__(self, latitude: float, longitude: float, angle: float):

        self.latitude = latitude
        self.longitude = longitude
        self.angle = angle

    @property
    def latlong(self):
        '''Tuple of latitude and longitude'''
        return (self.latitude, self.longitude)

    def distance_from(self, observation: 'Observation') -> float:
        '''
            Calculates the distance between two observations
            Uses geopy.distance.distance

            Parameters
            ----------

            observation
                The other observation to calculate the distance from

            Returns
            -------

            The distance between the observations in metres
        '''
        return geopy.distance.distance(self.latlong, observation.latlong).m

# - Functions

def height(angle1: float, angle2: float, distance: float) -> float:
    '''
        Computes the height based on two observed distances and angle between them

        Parameters
        ----------

        angle1
            Angle in radians of inclination as observed from first observation site
        angle2
            Angle in radians of inclination as observed from the second observation site
        distance
            Distance between the two observation sites

        Returns
        -------

        The height as computed from the two observations
    '''

    return (distance * math.tan(angle1) * math.tan(angle2))/(math.tan(angle1) - math.tan(angle2))

def obsv_height(obsv1: Observation, obsv2: Observation) -> float:
    '''
        Computes the height based on two observations

        Parameters
        ----------

        obsv1
            An observation
        obsv2
            An observation

        Returns
        -------

        The height as predicted from the observations
    '''

    if obsv1.angle < obsv2.angle:
        # Switch if angles aren't the right way around
        obsv1, obsv2 = obsv2, obsv1

    distance_between = obsv1.distance_from(obsv2)

    return height(obsv1.angle, obsv2.angle, distance_between)

def load_data(filename: str) -> Dict[str, Observation]:
    '''
        Loads data from csv file in expected format

        Parameters
        ----------

        filename
            The filename of the csv file to load

        Returns
        -------

        A dictionary mapping site names to observations
    '''

    # Instantiate empty observation dict
    observations = {}

    with open(filename) as file:
        # Open up CSV file
        reader = csv.DictReader(file)
        # For rows in csv file
        for row in reader:
            # Normal row processing
            observations[row["Site"]] = Observation(float(row["Latitude"]), float(row["Longitude"]), float(row["Inclination Angle (Rad)"]))

    return observations

# - Main

if __name__ == "__main__":

    # Get observations
    observations = load_data("observations.csv")

    # Approximate eye height
    approx_height = 1.68 # m

    # Set as variables for clarity
    # South of Hight
    a1 = observations["A1"]
    a2 = observations["A2"]
    a3 = observations["A3"]
    # Ilam Field
    b1 = observations["B1"]
    b2 = observations["B2"]

    # Calculate heights
    # Add an approximate 1.
    a1_a2 = obsv_height(a1, a2) + approx_height
    a1_a3 = obsv_height(a1, a3) + approx_height
    a2_a3 = obsv_height(a2, a3) + approx_height
    b1_b2 = obsv_height(b1, b2) + approx_height

    # Mean with half-range uncertainty
    final = mean([a1_a2, a1_a3, a2_a3, b1_b2])

    # Print results
    print("South of Hight: ")
    print(f"    A1-A2: {a1_a2:.2f} m")
    print(f"    A1-A3: {a1_a3:.2f} m")
    print(f"    A2-A3: {a2_a3:.2f} m")

    print("\nIlam Field: ")
    print(f"    B1-B2: {b1_b2:.2f} m")

    print("\nMean: ")
    print(f"    {final.value:.2f} m ")

    print("\nMean with Uncertainty:")
    print(f"    {final} m ")