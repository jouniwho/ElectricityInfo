import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";


type HourlyElectricityData = {
    startTime: string;
    productionAmount: number;
    id: number;
    date: string;
    hourlyPrice: number;
    consumptionAmount: number | null;
  }[];


  const Dailydatachart: React.FC<{ selectedDate: string }> = ({ selectedDate }) => {
  const [hourlyData, setHourlyData] = useState<HourlyElectricityData>([]);
  const [loading, setLoading] = useState(false);
   // Debugging
  const DataFormater = (number: number) => {
    // Formatter from
    // https://stackoverflow.com/questions/52320447/recharts-set-y-axis-value-base-of-number-displayed
    if(number > 1000000000){
      return (number/1000000000).toString() + 'B';
    }else if(number > 1000000){
      return (number/1000000).toString() + 'M';
    }else if(number > 1000){
      return (number/1000).toString() + 'K';
    }else{
      return number.toString();
    }
  }
  useEffect(() => {
    if (!selectedDate) return;
  
    setLoading(true);
    fetch(`http://127.0.0.1:8000/api/day-stats/${selectedDate}`)
      .then((res) => res.json())
      .then((json) => {
        // Check if `json` is an array and set state
        if (Array.isArray(json)) {
          setHourlyData(json);
        } else {
          console.error("Unexpected API response:", json);
          setHourlyData([]);
        }
  
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching hourly data:", error);
        setHourlyData([]);
        setLoading(false);
      });
  }, [selectedDate]);

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold text-center">Hourly Data for {selectedDate}</h2>

      {loading ? (
        <p className="text-center">Loading data...</p>
      ) : hourlyData.length > 0 ? (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={hourlyData}>
            <XAxis dataKey="startTime" tickFormatter={(time) => new Date(time).getHours() + ":00"} />
            <YAxis yAxisId="left" tickFormatter={DataFormater} />
            <YAxis 
              yAxisId="right" 
              orientation="right" 
              tickFormatter={(value) => `${value.toFixed(2)}`} 
            />
            <Tooltip />
            <Line 
              yAxisId="left" 
              type="monotone" 
              dataKey="productionAmount" 
              stroke="#8884d8" 
              name="Production (MWh)" 
            />
            <Line 
              yAxisId="left" 
              type="monotone" 
              dataKey="consumptionAmount" 
              stroke="#82ca9d" 
              name="Consumption (MWh)" 
            />
            <Line 
              yAxisId="right" 
              type="monotone" 
              dataKey="hourlyPrice" 
              stroke="#ff7300" 
              name="Hourly Price (€/MWh)" 
            />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-center">No hourly data available for {selectedDate}.</p>
      )}
    </div>
  );
};

export default Dailydatachart;
