import { useState, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";

const API_URL = "http://localhost:8000";

interface IngestResult {
  success: boolean;
  total: number;
  lojas: string[];
  periodo: { inicio: string; fim: string };
  message: string;
}

const UploadCSV = () => {
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IngestResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f && f.name.endsWith(".csv")) setFile(f);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) { setFile(f); setResult(null); setError(null); }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_URL}/ingest/csv`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        setError(err.detail || "Erro ao processar o arquivo.");
        return;
      }

      const data: IngestResult = await res.json();
      setResult(data);
    } catch {
      setError("Erro ao conectar com a API. Verifique se o backend está rodando.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6 animate-fade-in">
      <h2 className="text-2xl font-semibold tracking-tight">Upload de CSV</h2>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle className="text-base">Importar Avaliações</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-10 text-center transition-colors cursor-pointer ${
              dragging ? "border-primary bg-primary/5" : "border-border hover:border-muted-foreground"
            }`}
            onClick={() => document.getElementById("csv-input")?.click()}
          >
            <input
              id="csv-input"
              type="file"
              accept=".csv"
              className="hidden"
              onChange={handleFileChange}
            />
            <Upload className="mx-auto h-10 w-10 text-muted-foreground mb-3" />
            {file ? (
              <div className="flex items-center justify-center gap-2 text-foreground">
                <FileText className="h-4 w-4" />
                <span className="text-sm font-medium">{file.name}</span>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                Arraste um arquivo CSV ou clique para selecionar
              </p>
            )}
          </div>

          <div className="rounded-md bg-secondary/50 p-4 text-xs text-muted-foreground space-y-1">
            <p className="font-medium text-secondary-foreground text-sm mb-2">Colunas esperadas:</p>
            <code className="block">texto_avaliacao, nota, data, loja_id</code>
          </div>

          <Button
            onClick={handleUpload}
            disabled={!file || loading}
            className="w-full gradient-primary text-primary-foreground"
          >
            {loading ? "Processando..." : "Enviar Arquivo"}
          </Button>
        </CardContent>
      </Card>

      {error && (
        <Card className="glass-card border-destructive/30 animate-fade-in">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-destructive" />
              <span className="text-sm text-destructive">{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {result && (
        <Card className="glass-card animate-fade-in">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3 mb-4">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <span className="font-medium">Upload realizado com sucesso!</span>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center mb-4">
              <div>
                <p className="text-2xl font-bold">{result.total}</p>
                <p className="text-xs text-muted-foreground">Avaliações</p>
              </div>
              <div>
                <p className="text-2xl font-bold">{result.lojas.length}</p>
                <p className="text-xs text-muted-foreground">Lojas</p>
              </div>
              <div>
                <p className="text-sm font-bold">{result.periodo.inicio}</p>
                <p className="text-xs text-muted-foreground">até {result.periodo.fim}</p>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">
              Lojas: {result.lojas.join(", ")}
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default UploadCSV;