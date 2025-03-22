from prometheus_client import Counter, Histogram, Gauge, start_http_server
from typing import Dict, Any
import time
from ..config.settings import PROMETHEUS_PORT

class MetricsCollector:
    def __init__(self):
        # Initialize Prometheus metrics
        self.analysis_counter = Counter(
            'webpage_analysis_total',
            'Total number of webpage analyses performed'
        )
        
        self.execution_counter = Counter(
            'maintenance_execution_total',
            'Total number of maintenance executions'
        )
        
        self.verification_counter = Counter(
            'maintenance_verification_total',
            'Total number of maintenance verifications'
        )
        
        self.analysis_duration = Histogram(
            'webpage_analysis_duration_seconds',
            'Time taken for webpage analysis',
            buckets=[1, 5, 10, 30, 60]
        )
        
        self.execution_duration = Histogram(
            'maintenance_execution_duration_seconds',
            'Time taken for maintenance execution',
            buckets=[1, 5, 10, 30, 60]
        )
        
        self.seo_score = Gauge(
            'webpage_seo_score',
            'SEO score of the webpage (0-100)'
        )
        
        self.performance_score = Gauge(
            'webpage_performance_score',
            'Performance score of the webpage (0-100)'
        )
        
        # Start Prometheus server
        start_http_server(PROMETHEUS_PORT)
    
    def record_analysis(self, analysis: Dict[str, Any]):
        """Record metrics for webpage analysis."""
        self.analysis_counter.inc()
        
        # Record SEO score if available
        if 'seo_score' in analysis:
            self.seo_score.set(analysis['seo_score'])
        
        # Record performance metrics
        if 'performance_metrics' in analysis:
            metrics = analysis['performance_metrics']
            if 'load_time' in metrics:
                self.performance_score.set(100 - min(metrics['load_time'] / 2, 100))
    
    def record_execution(self, execution_steps: str):
        """Record metrics for maintenance execution."""
        self.execution_counter.inc()
        
        # Record execution duration
        start_time = time.time()
        # Simulate execution time (replace with actual execution)
        time.sleep(1)
        duration = time.time() - start_time
        self.execution_duration.observe(duration)
    
    def record_verification(self, verification: str):
        """Record metrics for maintenance verification."""
        self.verification_counter.inc()
        
        # Record verification duration
        start_time = time.time()
        # Simulate verification time (replace with actual verification)
        time.sleep(1)
        duration = time.time() - start_time
        self.execution_duration.observe(duration)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics values."""
        return {
            "analysis_count": self.analysis_counter._value.get(),
            "execution_count": self.execution_counter._value.get(),
            "verification_count": self.verification_counter._value.get(),
            "seo_score": self.seo_score._value.get(),
            "performance_score": self.performance_score._value.get()
        } 