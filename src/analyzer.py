"""AI-powered financial analysis using OpenAI GPT-4.5"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from openai import OpenAI

from config import config
from utils import FileManager, DataProcessor, Traceability, DateHelper, setup_logging

logger = logging.getLogger(__name__)


class FinancialAnalyzer:
    """Analyze financial documents using AI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.file_manager = FileManager(config.DATA_DIR, config.REPORTS_DIR)
        self.traceability = Traceability()
        self.processor = DataProcessor()
    
    def analyze_budget_allocation_anomalies(self, documents: List[Path]) -> Dict[str, Any]:
        """Detect inappropriate budget allocations"""
        logger.info("Analyzing budget allocation anomalies...")
        
        analysis_results = {
            "type": "budget_allocation_anomalies",
            "timestamp": datetime.now().isoformat(),
            "findings": [],
            "recommendations": []
        }
        
        for doc_path in documents:
            try:
                text = self.processor.extract_text_from_file(doc_path)
                if not text:
                    continue
                
                # Prepare prompt for anomaly detection
                prompt = f"""
                財政分析: 以下の予算書から不適切な予算配分を検出してください。
                
                文書: {doc_path.name}
                
                内容:
                {text[:5000]}  # 最初の5000文字に制限
                
                以下の点について分析し、JSON形式で結果を返してください:
                1. 異常な支出増減（前年度比）
                2. 予算配分の効率性
                3. 問題のある配分項目
                4. 納税者への影響
                
                JSON形式で以下のスキーマで返してください:
                {{
                    "anomalies": [
                        {{"category": "...", "issue": "...", "severity": "high/medium/low", "impact": "..."}}
                    ],
                    "efficiency_score": 0.0-1.0,
                    "recommendations": ["..."]
                }}
                """
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2000
                )
                
                result = response.choices[0].message.content
                
                # Parse JSON result
                try:
                    json_result = json.loads(result)
                    analysis_results["findings"].extend(json_result.get("anomalies", []))
                    analysis_results["recommendations"].extend(json_result.get("recommendations", []))
                    
                    # Add traceability
                    self.traceability.add_trace(
                        analysis_type="budget_allocation_anomalies",
                        finding=f"Found {len(json_result.get('anomalies', []))} anomalies",
                        source_file=doc_path.name,
                        confidence=0.85
                    )
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse AI response for {doc_path.name}")
            
            except Exception as e:
                logger.error(f"Error analyzing {doc_path.name}: {e}")
        
        return analysis_results
    
    def analyze_expenditure_trends(self, documents: List[Path]) -> Dict[str, Any]:
        """Analyze year-over-year expenditure trends"""
        logger.info("Analyzing expenditure trends...")
        
        analysis_results = {
            "type": "expenditure_trends",
            "timestamp": datetime.now().isoformat(),
            "trends": [],
            "predictions": []
        }
        
        for doc_path in documents:
            try:
                text = self.processor.extract_text_from_file(doc_path)
                if not text:
                    continue
                
                prompt = f"""
                支出傾向分析: 以下の決算書から支出傾向を分析してください。
                
                文書: {doc_path.name}
                
                内容:
                {text[:5000]}
                
                以下の点について分析し、JSON形式で結果を返してください:
                1. 年度間の支出パターン変化
                2. 主要支出項目の傾向
                3. 効率性の推移
                4. 今後の予測
                
                JSON形式で以下のスキーマで返してください:
                {{
                    "trends": [
                        {{"category": "...", "change_percentage": 0.0, "direction": "up/down/stable"}}
                    ],
                    "predictions": ["..."],
                    "key_insights": ["..."]
                }}
                """
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2000
                )
                
                result = response.choices[0].message.content
                
                try:
                    json_result = json.loads(result)
                    analysis_results["trends"].extend(json_result.get("trends", []))
                    analysis_results["predictions"].extend(json_result.get("predictions", []))
                    
                    self.traceability.add_trace(
                        analysis_type="expenditure_trends",
                        finding=f"Identified {len(json_result.get('trends', []))} trends",
                        source_file=doc_path.name,
                        confidence=0.82
                    )
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse AI response for {doc_path.name}")
            
            except Exception as e:
                logger.error(f"Error analyzing trends in {doc_path.name}: {e}")
        
        return analysis_results
    
    def analyze_department_anomalies(self, documents: List[Path]) -> Dict[str, Any]:
        """Detect anomalies in specific departments"""
        logger.info("Analyzing department-level anomalies...")
        
        analysis_results = {
            "type": "department_anomalies",
            "timestamp": datetime.now().isoformat(),
            "departments": {}
        }
        
        for doc_path in documents:
            try:
                text = self.processor.extract_text_from_file(doc_path)
                if not text:
                    continue
                
                prompt = f"""
                部門別異常検知: 以下の予算書から部門別の異常支出を検出してください。
                
                文書: {doc_path.name}
                
                内容:
                {text[:5000]}
                
                以下の部門について詳細に分析してください:
                1. 福祉（社会保障）
                2. 教育
                3. 土木・インフラ
                4. 行政管理
                5. その他
                
                JSON形式で以下のスキーマで返してください:
                {{
                    "departments": {{
                        "welfare": {{"anomalies": [...], "status": "normal/warning/critical"}},
                        "education": {{"anomalies": [...], "status": "normal/warning/critical"}},
                        ...
                    }}
                }}
                """
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2500
                )
                
                result = response.choices[0].message.content
                
                try:
                    json_result = json.loads(result)
                    analysis_results["departments"].update(json_result.get("departments", {}))
                    
                    self.traceability.add_trace(
                        analysis_type="department_anomalies",
                        finding=f"Analyzed {len(json_result.get('departments', {}))} departments",
                        source_file=doc_path.name,
                        confidence=0.80
                    )
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse AI response for {doc_path.name}")
            
            except Exception as e:
                logger.error(f"Error analyzing departments in {doc_path.name}: {e}")
        
        return analysis_results
    
    def generate_executive_summary(self, documents: List[Path]) -> Dict[str, Any]:
        """Generate automatic summary of expenditure content"""
        logger.info("Generating executive summary...")
        
        summary_results = {
            "type": "executive_summary",
            "timestamp": datetime.now().isoformat(),
            "summary": "",
            "key_points": [],
            "recommendations": []
        }
        
        all_text = ""
        for doc_path in documents:
            try:
                text = self.processor.extract_text_from_file(doc_path)
                all_text += f"\n[{doc_path.name}]\n{text[:3000]}\n"
            except Exception as e:
                logger.error(f"Error reading {doc_path.name}: {e}")
        
        if not all_text:
            return summary_results
        
        try:
            prompt = f"""
            武豊町財政分析概要: 以下の財政資料から、納税者向けの分かりやすい概要を作成してください。
            
            資料:
            {all_text[:8000]}
            
            以下の内容を含む、分かりやすい概要を作成してください:
            1. 予算の全体像
            2. 主要な支出項目
            3. 納税者への影響
            4. 改善提案
            
            JSON形式で以下のスキーマで返してください:
            {{
                "summary": "...",
                "key_points": ["...", "..."],
                "taxpayer_impact": "...",
                "recommendations": ["..."]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            
            try:
                json_result = json.loads(result)
                summary_results["summary"] = json_result.get("summary", "")
                summary_results["key_points"] = json_result.get("key_points", [])
                summary_results["recommendations"] = json_result.get("recommendations", [])
                
                self.traceability.add_trace(
                    analysis_type="executive_summary",
                    finding="Executive summary generated",
                    source_file="multiple",
                    confidence=0.75
                )
            except json.JSONDecodeError:
                logger.warning("Failed to parse executive summary")
        
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
        
        return summary_results
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        logger.info("Generating comprehensive report...")
        
        # Get all available documents
        documents = list(config.DATA_DIR.glob("*"))
        
        if not documents:
            logger.warning("No documents found for analysis")
            return {"error": "No documents to analyze"}
        
        # Run all analyses
        report = {
            "timestamp": datetime.now().isoformat(),
            "fiscal_year": config.ANALYSIS_YEAR,
            "document_count": len(documents),
            "documents": [d.name for d in documents],
            "analyses": {
                "budget_allocation": self.analyze_budget_allocation_anomalies(documents),
                "expenditure_trends": self.analyze_expenditure_trends(documents),
                "department_anomalies": self.analyze_department_anomalies(documents),
                "executive_summary": self.generate_executive_summary(documents)
            },
            "traceability": self.traceability.get_traces()
        }
        
        # Save report
        report_path = self.file_manager.save_report("taketo_financial_analysis", report)
        logger.info(f"Report saved to: {report_path}")
        
        return report


def main():
    """Main execution for analyzer"""
    setup_logging(config.LOG_LEVEL, config.LOGS_DIR)
    
    analyzer = FinancialAnalyzer()
    report = analyzer.generate_comprehensive_report()
    
    logger.info("Analysis completed successfully")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
