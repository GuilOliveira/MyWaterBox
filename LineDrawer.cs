using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LineDrawer : MonoBehaviour
{
    public GameObject LinePrefabs;
    public LayerMask CantDrawOverLayer;
    int CantDrawOverLayerIndex;


    public float LinePointsMinDistance;
    public float LineWidth;
    public Gradient LineColor;


    Line currentLine;


    private void Start()
    {
        CantDrawOverLayerIndex = LayerMask.NameToLayer("CantDrawOver");
    }


    private void Update()
    {
        if (Input.GetMouseButtonDown(0))
            BeginDraw();

        if (currentLine != null)
            Draw();

        if (Input.GetMouseButtonUp(0))
            EndDraw();
    }


    private void BeginDraw()
    {
        currentLine = Instantiate(LinePrefabs, this.transform).GetComponent<Line>();


        currentLine.SetLineColor(LineColor);
        currentLine.SetLineWidth(LineWidth);
        currentLine.SetPointsMinDistance(LinePointsMinDistance);
        currentLine.UsePhysics(false);
    }

    private void Draw()
    {
        Vector2 MousePos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        RaycastHit2D hit = Physics2D.CircleCast(MousePos, LineWidth / 3f, Vector2.zero, 1f, CantDrawOverLayer);

        if (hit)
            EndDraw();
        else
            currentLine.AddPoint(MousePos);
    }

    private void EndDraw()
    {
        if(currentLine != null)
        {
            if(currentLine.pointsCount < 2)
            {
                Destroy(currentLine.gameObject);
            }
            else
            {
                currentLine.gameObject.layer = CantDrawOverLayerIndex;
                currentLine.UsePhysics(true);
                currentLine = null;
            }
        }
    }
}
