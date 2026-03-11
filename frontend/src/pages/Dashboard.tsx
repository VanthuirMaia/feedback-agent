import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Star, TrendingUp, TrendingDown, BarChart3 } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line,
} from "recharts";

const API_URL = "http://localhost:8000";

interface DashboardData {
  total: number;
  media_geral: number;
  melhor_loja: { nome: string; media: number };
  pior_loja: { nome: string; media: number };
  por_loja: { loja_id: string; total: number; media: number }[];
  evolucao: { mes: string; total: number; media: number }[];
}

const Dashboard = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/dashboard/summary`)
      .then((res) => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(setData)
      .catch(() => setError(true));
  }, []);

  if (error) return (
    <div className="p-6 text-muted-foreground text-sm">
      Nenhum dado carregado. Faça upload de um CSV primeiro.
    </div>
  );

  if (!data) return (
    <div className="p-6 text-muted-foreground text-sm">Carregando...</div>
  );

  const metrics = [
    { title: "Total de Avaliações", value: data.total.toLocaleString(), icon: BarChart3, color: "text-primary" },
    { title: "Média Geral", value: data.media_geral.toFixed(1), icon: Star, color: "text-warning" },
    { title: "Melhor Nota", value: data.melhor_loja.nome, sub: `${data.melhor_loja.media} ★`, icon: TrendingUp, color: "text-success" },
    { title: "Pior Nota", value: data.pior_loja.nome, sub: `${data.pior_loja.media} ★`, icon: TrendingDown, color: "text-destructive" },
  ];

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <h2 className="text-2xl font-semibold tracking-tight">Dashboard</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((m) => (
          <Card key={m.title} className="glass-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{m.title}</CardTitle>
              <m.icon className={`h-4 w-4 ${m.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{m.value}</div>
              {m.sub && <p className="text-xs text-muted-foreground mt-1">{m.sub}</p>}
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-base">Média por Loja</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={data.por_loja}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(215 20% 18%)" />
                <XAxis dataKey="loja_id" stroke="hsl(215 15% 55%)" fontSize={12} />
                <YAxis domain={[0, 5]} stroke="hsl(215 15% 55%)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(220 18% 10%)",
                    border: "1px solid hsl(215 20% 18%)",
                    borderRadius: "8px",
                    color: "hsl(210 20% 92%)",
                  }}
                />
                <Bar dataKey="media" fill="hsl(210 72% 36%)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-base">Evolução ao Longo do Tempo</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={data.evolucao}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(215 20% 18%)" />
                <XAxis dataKey="mes" stroke="hsl(215 15% 55%)" fontSize={12} />
                <YAxis domain={[0, 5]} stroke="hsl(215 15% 55%)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(220 18% 10%)",
                    border: "1px solid hsl(215 20% 18%)",
                    borderRadius: "8px",
                    color: "hsl(210 20% 92%)",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="media"
                  stroke="hsl(195 70% 42%)"
                  strokeWidth={2}
                  dot={{ fill: "hsl(195 70% 42%)", r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;