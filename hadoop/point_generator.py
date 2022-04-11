from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import seaborn as sns

X, y, centers = make_blobs(n_samples=1500000, centers=3, cluster_std=88.5, random_state=8, center_box=(-1000, 1000), return_centers=True)

pts = []
for e in X:
    pts.append((e[0].round(5), e[1].round(5)))
    
ctrs = []
for e in centers:
    pts.append(e[0].round(5), e[1].round(5))
    
with open('points.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in pts))
    
with open('centers.txt', 'w') as cfp:
    cfp.write('\n'.join('%s %s' % x for x in ctrs))
    
ax = sns.scatterplot(X[:,0], X[:,1], hue=y, s=1, alpha=0.5)
plt.scatter(centers[:,0], centers[:,1], color='r')
