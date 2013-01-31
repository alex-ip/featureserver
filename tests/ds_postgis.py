import re
import unittest
import datasource

try:
    import psycopg2 as psycopg
except:
    import psycopg

from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request

from featureserver.datasource.PostGIS import PostGIS


class PostGISTestCase(unittest.TestCase, datasource.Base):
    
    @property
    def table_schema(self):
        return """CREATE TABLE fs_point (id SERIAL, name TEXT, salary INTEGER );"""
    @property
    def table_tuples(self):
        return [
                "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Carrasquillo', 109000, ST_GeomFromText('POINT(8.515048 47.461261)', 4326));",
                "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Fewell', 129000, ST_GeomFromText('POINT(7.581210 47.379493)', 4326));",
                "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Mcmillon', 125000, ST_GeomFromText('POINT(7.383456 46.983736)', 4326));",
                "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Sykes', 112000, ST_GeomFromText('POINT(7.877841 46.384567)', 4326));",
                "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Steger', 130000, ST_GeomFromText('POINT(8.811679 46.788513)', 4326));",
                "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Conroy', 120000, ST_GeomFromText('POINT(8.157992 47.081082)', 4326));",
                ]

    @classmethod
    def setUpClass(cls):
        ''' '''
    
    @classmethod
    def tearDownClass(cls):
        ''' '''

    def setUp(self):
        self._connection = psycopg.connect('host=localhost dbname=featureserver user=michel')
        cursor = self._connection.cursor()
        
        cursor.execute(self.table_schema)
        cursor.execute("SELECT AddGeometryColumn ('featureserver', 'public', 'fs_point', 'geom',4326, 'POINT', 2, false);")
        
        for data in self.table_tuples:
            cursor.execute(data)
        
        
        cursor.close()
        self._connection.commit()

        self._fs = Server({
                         'fs_point' : PostGIS('fs_point', **{
                                              'type': 'PostGIS',
                                              'dsn' : 'host=localhost dbname=featureserver user=michel',
                                              'layer' : 'fs_point',
                                              'fid' : 'id',
                                              'geometry' : 'geom',
                                              'srid' : 4326,
                                              'srid_out' : 4326,
                                              'encoding' : 'utf-8',
                                              'attribut_cols' : 'name',
                                              'additional_cols' : ''
                                              })
                         }, metadata = {'default_output':'WFS', 'default_exception':'WFS'})
    
    def tearDown(self):
        cursor = self._connection.cursor()
        
        cursor.execute("SELECT DropGeometryColumn('featureserver', 'public', 'fs_point', 'geom');")
        cursor.execute("DROP TABLE fs_point")        
        
        cursor.close()
        
        self._connection.commit()
        self._connection.close()

    
    
    @property
    def data_empty(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> </wfs:FeatureCollection>"""

    @property
    def data_features(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:salary>109000</fs:salary><fs:name>Carrasquillo</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:salary>112000</fs:salary><fs:name>Sykes</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="5"><fs:fs_point fid="5"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.811679,46.788513</gml:coordinates></gml:Point><fs:salary>130000</fs:salary><fs:name>Steger</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="6"><fs:fs_point fid="6"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.157992,47.081082</gml:coordinates></gml:Point><fs:salary>120000</fs:salary><fs:name>Conroy</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_features_ordered(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="4"><fs:fs_point fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:salary>112000</fs:salary><fs:name>Sykes</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="5"><fs:fs_point fid="5"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.811679,46.788513</gml:coordinates></gml:Point><fs:salary>130000</fs:salary><fs:name>Steger</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="6"><fs:fs_point fid="6"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.157992,47.081082</gml:coordinates></gml:Point><fs:salary>120000</fs:salary><fs:name>Conroy</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:salary>109000</fs:salary><fs:name>Carrasquillo</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_features_queryable(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_feature_two(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_features_bbox(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:salary>112000</fs:salary><fs:name>Sykes</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_insert_single_response(self):
        return """<?xml version="1.0" encoding="UTF-8"?> <wfs:TransactionResponse version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:og="http://opengeo.org" xmlns:ogc="http://www.opengis.net/ogc" xmlns:tiger="http://www.census.gov" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:nurc="http://www.nurc.nato.int" xmlns:sde="http://geoserver.sf.net" xmlns:analytics="http://opengeo.org/analytics" xmlns:wfs="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:it.geosolutions="http://www.geo-solutions.it" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sf="http://www.openplans.org/spearfish" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:za="http://opengeo.org/za" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:tike="http://opengeo.org/#tike"> <wfs:TransactionSummary> <wfs:totalInserted>1</wfs:totalInserted> <wfs:totalUpdated>0</wfs:totalUpdated> <wfs:totalDeleted>0</wfs:totalDeleted> <wfs:totalReplaced>0</wfs:totalReplaced> </wfs:TransactionSummary> <wfs:TransactionResults/> <wfs:InsertResults><wfs:Feature handle=""><ogc:ResourceId fid="7"/></wfs:Feature></wfs:InsertResults><wfs:UpdateResults></wfs:UpdateResults><wfs:ReplaceResults></wfs:ReplaceResults><wfs:DeleteResults></wfs:DeleteResults><wfs:TransactionResult> <wfs:Status> <wfs:SUCCESS/></wfs:Status> </wfs:TransactionResult></wfs:TransactionResponse>"""
    @property
    def data_insert_single_feature(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="7"><fs:fs_point fid="7"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.65237703581,47.2491447055</gml:coordinates></gml:Point><fs:salary>None</fs:salary><fs:name>None</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_update_single_response(self):
        return """<?xml version="1.0" encoding="UTF-8"?> <wfs:TransactionResponse version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:og="http://opengeo.org" xmlns:ogc="http://www.opengis.net/ogc" xmlns:tiger="http://www.census.gov" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:nurc="http://www.nurc.nato.int" xmlns:sde="http://geoserver.sf.net" xmlns:analytics="http://opengeo.org/analytics" xmlns:wfs="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:it.geosolutions="http://www.geo-solutions.it" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sf="http://www.openplans.org/spearfish" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:za="http://opengeo.org/za" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:tike="http://opengeo.org/#tike"> <wfs:TransactionSummary> <wfs:totalInserted>0</wfs:totalInserted> <wfs:totalUpdated>1</wfs:totalUpdated> <wfs:totalDeleted>0</wfs:totalDeleted> <wfs:totalReplaced>0</wfs:totalReplaced> </wfs:TransactionSummary> <wfs:TransactionResults/> <wfs:InsertResults></wfs:InsertResults><wfs:UpdateResults><wfs:Feature handle=""><ogc:ResourceId fid="1"/></wfs:Feature></wfs:UpdateResults><wfs:ReplaceResults></wfs:ReplaceResults><wfs:DeleteResults></wfs:DeleteResults><wfs:TransactionResult> <wfs:Status> <wfs:SUCCESS/></wfs:Status> </wfs:TransactionResult></wfs:TransactionResponse>"""
    @property
    def data_update_single_feature(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:salary>90900</fs:salary><fs:name>Alfredo</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_delete_single_response(self):
        return """<?xml version="1.0" encoding="UTF-8"?> <wfs:TransactionResponse version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:og="http://opengeo.org" xmlns:ogc="http://www.opengis.net/ogc" xmlns:tiger="http://www.census.gov" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:nurc="http://www.nurc.nato.int" xmlns:sde="http://geoserver.sf.net" xmlns:analytics="http://opengeo.org/analytics" xmlns:wfs="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:it.geosolutions="http://www.geo-solutions.it" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sf="http://www.openplans.org/spearfish" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:za="http://opengeo.org/za" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:tike="http://opengeo.org/#tike"> <wfs:TransactionSummary> <wfs:totalInserted>0</wfs:totalInserted> <wfs:totalUpdated>0</wfs:totalUpdated> <wfs:totalDeleted>1</wfs:totalDeleted> <wfs:totalReplaced>0</wfs:totalReplaced> </wfs:TransactionSummary> <wfs:TransactionResults/> <wfs:InsertResults></wfs:InsertResults><wfs:UpdateResults></wfs:UpdateResults><wfs:ReplaceResults></wfs:ReplaceResults><wfs:DeleteResults><wfs:Feature handle=""><ogc:ResourceId fid="2"/></wfs:Feature></wfs:DeleteResults><wfs:TransactionResult> <wfs:Status> <wfs:SUCCESS/></wfs:Status> </wfs:TransactionResult></wfs:TransactionResponse>"""
    
    @property
    def data_delete_multiple_response(self):
        return """<?xml version="1.0" encoding="UTF-8"?> <wfs:TransactionResponse version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:og="http://opengeo.org" xmlns:ogc="http://www.opengis.net/ogc" xmlns:tiger="http://www.census.gov" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:nurc="http://www.nurc.nato.int" xmlns:sde="http://geoserver.sf.net" xmlns:analytics="http://opengeo.org/analytics" xmlns:wfs="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:it.geosolutions="http://www.geo-solutions.it" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sf="http://www.openplans.org/spearfish" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:za="http://opengeo.org/za" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:tike="http://opengeo.org/#tike"> <wfs:TransactionSummary> <wfs:totalInserted>0</wfs:totalInserted> <wfs:totalUpdated>0</wfs:totalUpdated> <wfs:totalDeleted>1</wfs:totalDeleted> <wfs:totalReplaced>0</wfs:totalReplaced> </wfs:TransactionSummary> <wfs:TransactionResults/> <wfs:InsertResults></wfs:InsertResults><wfs:UpdateResults></wfs:UpdateResults><wfs:ReplaceResults></wfs:ReplaceResults><wfs:DeleteResults><wfs:Feature handle=""><ogc:ResourceId fid="1"/><ogc:ResourceId fid="3"/></wfs:Feature></wfs:DeleteResults><wfs:TransactionResult> <wfs:Status> <wfs:SUCCESS/></wfs:Status> </wfs:TransactionResult></wfs:TransactionResponse>"""







class SpatiaLiteWFS110TestCase(PostGISTestCase):
    
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)
    
    def test_keyword_by_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/2.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)

    def test_get_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs", params = {'version':'1.1.0', 'request':'GetFeature', 'typename':'fs_point'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)

    def test_get_bbox(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {'service':'WFS','version':'1.1.0', 'request':'GetFeature', 'typename':'fs_point', 'bbox':'7.0,46.0,8.0,47.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_bbox)

    def test_post_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point" srsName="EPSG:4326" /></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)

    def test_post_by_gml_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point" srsName="EPSG:4326" /><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:GmlObjectId xmlns:gml="http://www.opengis.net/gml" gml:id="2"/></ogc:Filter></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)

    def test_post_by_feat_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point" srsName="EPSG:4326" /><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:FeatureId fid="2"/></ogc:Filter></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)

    def test_post_insert_single(self):
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Insert><fs_point xmlns:feature="http://example.com/featureserver"><geom><gml:Point xmlns:gml="http://www.opengis.net/gml" srsName="EPSG:4326"><gml:pos>8.65237703580643 47.2491447055323</gml:pos></gml:Point></geom></fs_point></wfs:Insert></wfs:Transaction>')
        transactions = self.ds_process('fs_point', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_insert_single_response)
        
        # test if feature was inserted into database by querying by its id
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/7.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_insert_single_feature)

    def test_post_update_single(self):
        # update feature 1
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Update typeName="fs_point"><wfs:Property><wfs:Name>name</wfs:Name><wfs:Value>Alfredo</wfs:Value></wfs:Property><wfs:Property><wfs:Name>salary</wfs:Name><wfs:Value>90900</wfs:Value></wfs:Property><ogc:Filter><ogc:FeatureId fid="1"/></ogc:Filter></wfs:Update></wfs:Transaction>')
        transactions = self.ds_process('fs_point', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_update_single_response)
        
        # test if feature was inserted into database by querying by its id
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/1.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_update_single_feature)

    def test_post_delete_single(self):
        # delete feature 2
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Delete typeName="fs_point"><ogc:Filter><ogc:FeatureId fid="2"/></ogc:Filter></wfs:Delete></wfs:Transaction>')
        transactions = self.ds_process('fs_point', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_delete_single_response)
        
        # test if feature is gone from database
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/2.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_empty)

    def test_post_delete_multiple(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Delete typeName="fs_point"><ogc:Filter><ogc:FeatureId fid="1"/><ogc:FeatureId fid="3"/></ogc:Filter></wfs:Delete></wfs:Transaction>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_delete_multiple_response)

    def test_sort(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {
                                                   'version':'1.1.0',
                                                   'service':'WFS',
                                                   'request':'GetFeature',
                                                   'typename':'fs_point',
                                                   'outputformat':'WFS',
                                                   'sortby':'name_DESC,salary_ASC'
                                                   }))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_ordered)

    def test_constraints(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {
                                                   'version':'1.1.0',
                                                   'service':'WFS',
                                                   'request':'GetFeature',
                                                   'typename':'fs_point',
                                                   'outputformat':'WFS',
                                                   'queryable':'name,salary',
                                                   'name__like':'ll',
                                                   'salary__gte':'120000'
                                                   }))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_queryable)


class SpatiaLiteWFS200TestCase(PostGISTestCase):
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'2.0.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)
    
    def test_keyword_by_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/2.wfs", params = {'version':'2.0.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)
    
    def test_get_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs", params = {'version':'2.0.0', 'request':'GetFeature', 'typenames':'fs_point'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)
    
    def test_get_bbox(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {'service':'WFS','version':'2.0.0', 'request':'GetFeature', 'typenames':'fs_point', 'bbox':'7.0,46.0,8.0,47.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_bbox)
    
    def test_post_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeNames="fs_point" srsName="EPSG:4326" /></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)
    
    @unittest.skip("Not supported in WFS 2.x")
    def test_post_by_gml_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point" srsName="EPSG:4326" /><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:GmlObjectId xmlns:gml="http://www.opengis.net/gml" gml:id="2"/></ogc:Filter></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)

    
    def test_post_by_feat_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeNames="fs_point" srsName="EPSG:4326" /><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:ResourceId rid="2"/></ogc:Filter></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)
    
    def test_post_insert_single(self):
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Insert><fs_point xmlns:feature="http://example.com/featureserver"><geom><gml:Point xmlns:gml="http://www.opengis.net/gml" srsName="EPSG:4326"><gml:pos>8.65237703580643 47.2491447055323</gml:pos></gml:Point></geom></fs_point></wfs:Insert></wfs:Transaction>')
        transactions = self.ds_process('fs_point', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_insert_single_response)
        
        # test if feature was inserted into database by querying by its id
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/7.wfs", params = {'version':'2.0.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_insert_single_feature)
    
    
    def test_post_update_single(self):
        # update feature 1
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Update typeName="fs_point"><wfs:Property><wfs:ValueReference>name</wfs:ValueReference><wfs:Value>Alfredo</wfs:Value></wfs:Property><wfs:Property><wfs:ValueReference>salary</wfs:ValueReference><wfs:Value>90900</wfs:Value></wfs:Property><ogc:Filter><ogc:FeatureId fid="1"/></ogc:Filter></wfs:Update></wfs:Transaction>')
        transactions = self.ds_process('fs_point', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_update_single_response)
        
        # test if feature was inserted into database by querying by its id
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/1.wfs", params = {'version':'2.0.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_update_single_feature)
    
    
    def test_post_delete_single(self):
        # delete feature 2
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Delete typeName="fs_point"><ogc:Filter><ogc:ResourceId rid="2"/></ogc:Filter></wfs:Delete></wfs:Transaction>')
        transactions = self.ds_process('fs_point', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_delete_single_response)
        
        # test if feature is gone from database
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/2.wfs", params = {'version':'2.0.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_empty)
    
    
    def test_post_delete_multiple(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="2.0.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Delete typeName="fs_point"><ogc:Filter><ogc:ResourceId rid="1"/><ogc:ResourceId rid="3"/></ogc:Filter></wfs:Delete></wfs:Transaction>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_delete_multiple_response)
    
    
    def test_sort(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {
                                                   'version':'2.0.0',
                                                   'service':'WFS',
                                                   'request':'GetFeature',
                                                   'typenames':'fs_point',
                                                   'outputformat':'WFS',
                                                   'sortby':'name_DESC,salary_ASC'
                                                   }))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_ordered)
    
    def test_constraints(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {
                                                   'version':'2.0.0',
                                                   'service':'WFS',
                                                   'request':'GetFeature',
                                                   'typenames':'fs_point',
                                                   'outputformat':'WFS',
                                                   'queryable':'name,salary',
                                                   'name__like':'ll',
                                                   'salary__gte':'120000'
                                                   }))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_queryable)




def test_suites():
    return [unittest.TestLoader().loadTestsFromTestCase(SpatiaLiteWFS110TestCase), unittest.TestLoader().loadTestsFromTestCase(SpatiaLiteWFS200TestCase)]

