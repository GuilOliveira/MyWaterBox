using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Line : MonoBehaviour
{
    public LineRenderer lineRenderer;
    public EdgeCollider2D edgeCollider;
    public Rigidbody2D rb;

    [HideInInspector] public List<Vector2> points = new List<Vector2>();
    [HideInInspector] public int pointsCount = 0;

    private float pointsMinDistance = 0.1f;
    private float CircleColliderRaduis;


    public Vector2 GetLastPoint()
    {
        return (Vector2)lineRenderer.GetPosition(pointsCount - 1);
    }


    public void UsePhysics(bool usePhysic)
    {
        rb.isKinematic = !usePhysic;
    }


    public void SetLineColor(Gradient LineColor)
    {
        lineRenderer.colorGradient = LineColor;
    }


    public void SetLineWidth(float width)
    {
        lineRenderer.startWidth = width;
        lineRenderer.endWidth = width;


        edgeCollider.edgeRadius = width / 2f;
        CircleColliderRaduis = width / 2f;
    }



    public void AddPoint(Vector2 newPoint)
    {
        if (pointsCount >= 1 && Vector2.Distance(newPoint, GetLastPoint()) < pointsMinDistance)
            return;

        points.Add(newPoint);
        pointsCount++;

        // Add CircleCollider to the point
        CircleCollider2D circleCollider = this.gameObject.AddComponent<CircleCollider2D>();
        circleCollider.offset = newPoint;
        circleCollider.radius = CircleColliderRaduis;

        //LineRenderer
        lineRenderer.positionCount = pointsCount;
        lineRenderer.SetPosition(pointsCount - 1, newPoint);

        //EdgeCollider
        if (pointsCount > 1)
            edgeCollider.points = points.ToArray();
    }


    public void SetPointMinDistance(float distance)
    {
        pointsMinDistance = distance;
    }
}
