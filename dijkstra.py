import math
from collections import defaultdict
import heapq as heap


class Vertex:
    def __init__(self, num, name, y_pos, x_pos):
        self.num = num
        self.name = name
        self.y_pos = y_pos
        self.x_pos = x_pos


def dijkstra(G, startingNode, endingNode):
    visited = set()
    path = {}
    pq = []
    nodeCosts = defaultdict(lambda: float('inf'))
    nodeCosts[startingNode] = 0
    heap.heappush(pq, (0, startingNode))

    while pq:
        _, node = heap.heappop(pq)
        visited.add(node)

        for adjNode, weight in G[node]:
            if adjNode in visited:
                continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                path[adjNode] = node
                nodeCosts[adjNode] = newCost
                heap.heappush(pq, (newCost, adjNode))

    return path, nodeCosts[endingNode]


def GPSDistance(lat1, lon1, lat2, lon2):
  def haversin(x):
    return math.sin(x/2)**2
  return 2 * math.asin(math.sqrt(
      haversin(lat2-lat1) +
      math.cos(lat1) * math.cos(lat2) * haversin(lon2-lon1)))



radius = 6371    #Earth Radius in KM

class referencePoint:
    def __init__(self, scrX, scrY, lat, lng):
        self.scrX = scrX
        self.scrY = scrY
        self.lat = lat
        self.lng = lng


# Calculate global X and Y for top-left reference point
p0 = referencePoint(0, 0, 33.8, 33.7)
# Calculate global X and Y for bottom-right reference point
p1 = referencePoint(614, 864, 30.1, 36.3)


# This function converts lat and lng coordinates to GLOBAL X and Y positions
def latlngToGlobalXY(lat, lng):
    # Calculates x based on cos of average of the latitudes
    x = radius*lng*math.cos((p0.lat + p1.lat)/2)
    # Calculates y based on latitude
    y = radius*lat
    return {'x': x, 'y': y}

p0.pos = latlngToGlobalXY(p0.lat, p0.lng);

p1.pos = latlngToGlobalXY(p1.lat, p1.lng);

# This function converts lat and lng coordinates to SCREEN X and Y positions
def latlngToScreenXY(lat, lng):
    # Calculate global X and Y for projection point
    pos = latlngToGlobalXY(lat, lng)
    # Calculate the percentage of Global X position in relation to total global width
    perX = ((pos['x']-p0.pos['x'])/(p1.pos['x'] - p0.pos['x']))
    # Calculate the percentage of Global Y position in relation to total global height
    perY = ((pos['y']-p0.pos['y'])/(p1.pos['y'] - p0.pos['y']))

    # Returns the screen position based on reference points
    return {
        'x': int(p0.scrX + (p1.scrX - p0.scrX)*perX),
        'y': int(p0.scrY + (p1.scrY - p0.scrY)*perY)
    }


