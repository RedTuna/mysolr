#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""

from urllib import urlencode

class SolrQuery:
    """ Solr Query object
    """
    
    VALID_FACET_METHODS = ['fc','enum']
    VALID_FACET_DATE_OTHERS = ['before', 'after', 'between', 'none', 'all']
    VALID_FACET_DATE_INCLUDES = ['lower', 'upper', 'edge', 'outer', 'all']
    
    def __init__(self, **kwargs):
        """Solr Query object initialization
    
        Keyword arguments:
        q -- string containing the query to be used.
        start -- integer showing the starting position for the results.
        rows -- integer showing the number of results we want.
        op -- string to override default operator
        df -- string to override default search field
        facets -- list containing dictionaries with the following structure:
          {
            field -- field to use in the facet
            limit -- limit used for this field facet
            mincount -- min count used for this field facet
            sort -- sort used for this field facet
            prefix -- prefix used for this field facet
            missing --  missing param used for this field facet
            method -- method used for this facet fields
          }
        facet_limit -- general facet limit
        facet_mincount -- general facet min count
        facet_sort -- general facet sort
        facet_prefix -- general facet prefix
        facet_missing -- general facet missing parameter
        facet_method -- general facet method
        facet_dates -- list containing dictionaries with the following structure:
          {
            field -- field to use in this facet.date
            start -- start used in this facet.date
            end -- end used in this facet.date
            gap -- gap used in this facet.date
            hardend -- hardend used in this facet.date
            other -- other param used in this facet.date
            include -- include param used in this facet.date
          }
        facet_date_start -- general facet date start param
        facet_date_end -- general facet date end param
        facet_date_gap -- general facet date gap param
        facet_date_hardend -- general facet date hardend param
        facet_date_other -- general facet date other param
        facet_date_include -- general facet date include param
        facet_ranges -- list containing dictionaries with the following structure:
          {
            field -- field to use in this facet.range
            start -- start used in this facet.range
            end -- end used in this facet.range
            gap -- gap used in this facet.range
            hardend -- hardend used in this facet.range
            other -- other param used in this facet.range
            include -- include param used in this facet.range
          }
        facet_range_start -- general facet range start param
        facet_range_end -- general facet range end param
        facet_range_gap -- general facet range gap param
        facet_range_hardend -- general facet range hardend param
        facet_range_other -- general facet range other param
        facet_range_include -- general facet range include param
        facet_pivot -- list containing lists of fields to pivot
        fl -- list with the fields we want to return.
        sort -- string with the sorting we want to use for the result
        omit_header -- boolean param to decide if we want to receive search header or not
    
        """
        self.q = kwargs.get('q', None)
        self.start = kwargs.get('start', 0)
        self.rows = kwargs.get('rows', 10)
        self.op = kwargs.get('op', None)
        self.df = kwargs.get('df', None)
        self.facets = kwargs.get('facets', None)
        self.facet_limit = kwargs.get('facet_limit', None)
        self.facet_mincount = kwargs.get('facet_mincount', None)
        self.facet_sort = kwargs.get('facet_sort', None)
        self.facet_prefix = kwargs.get('facet_prefix', None)
        self.facet_missing = kwargs.get('facet_missing', None)
        self.facet_method = kwargs.get('facet_method', None)
        self.facet_dates = kwargs.get('facet_dates', None)
        self.facet_date_start = kwargs.get('facet_date_start', None)
        self.facet_date_end = kwargs.get('facet_date_end', None)
        self.facet_date_gap = kwargs.get('facet_date_gap', None)
        self.facet_date_hardend = kwargs.get('facet_date_hardend', None)
        self.facet_date_other = kwargs.get('facet_date_other', None)
        self.facet_date_include = kwargs.get('facet_date_include', None)
        self.facet_ranges = kwargs.get('facet_ranges', None)
        self.facet_range_start = kwargs.get('facet_range_start', None)
        self.facet_range_end = kwargs.get('facet_range_end', None)
        self.facet_range_gap = kwargs.get('facet_range_gap', None)
        self.facet_range_hardend = kwargs.get('facet_range_hardend', None)
        self.facet_range_other = kwargs.get('facet_range_other', None)
        self.facet_range_include = kwargs.get('facet_range_include', None)
        self.facet_pivot = kwargs.get('facet_pivot', None)
        self.fq = kwargs.get('fq', None)
        self.fl = kwargs.get('fl', None)
        self.sort = kwargs.get('sort', None)
        self.omit_header = kwargs.get('omit_header', None)
  
    def build(self):
        """
        """
        temp_query = '&'.join([self.__build_query(),
                               self.__build_query_start(),
                               self.__build_query_rows(),
                               self.__build_query_op(),
                               self.__build_query_df(),
                               self.__build_query_facets(),
                               self.__build_query_facet_dates(),
                               self.__build_query_facet_ranges(),
                               self. __build_query_facet_pivots(),
                               self.__build_query_return_fields(),
                               self.__build_query_sort(),
                               self.__build_query_facet_queries(),
                               self.__build_query_omit_header()])
        return '%s&wt=python' % (temp_query) 
    
    def __build_query(self):
        """
        """
        q = {}
        if self.q != None:
            q['q'] = self.q
        else:
            q['q'] = '*:*'
        q = urlencode(q)
        return q
    
    def __build_query_start(self):
        """
        """
        return 'start=%s' % (self.start)
    
    def __build_query_rows(self):
        """
        """
        return 'rows=%s' % (self.rows)
    
    def __build_query_op(self):
        """
        """
        op = ''
        if self.op != None:
            op = 'q.op=%s' % (self.op)
        return op
    
    def __build_query_df(self):
        """
        """
        df = ''
        if self.df != None:
            df = 'df=%s' % (self.df)
        return df
    
    def __build_query_facets(self):
        """
        """
        facets = ''
        if self.facets != None:
            facets = '&'.join(['facet.field=%s' % (facet['field']) for facet in self.facets])
            facets = 'facet=true&%s' % (facets)
            facets = '%s&%s' % (facets, self.__per_field_basis_facet_params())
            if self.facet_mincount != None:
                facets = '%s&facet.mincount=%s' % (facets, self.facet_mincount)
            if self.facet_limit != None:
                facets = '%s&facet.limit=%s' % (facets, self.facet_limit)
            if self.facet_sort != None:
                facets = '%s&facet.sort=%s' % (facets, urlencode(self.facet_sort))
            if self.facet_prefix != None:
                facets = '%s&facet.prefix=%s' % (facets, urlencode(self.facet_prefix))
            if self.facet_missing != None:
                temp_missing = 'facet.missing=true' if self.facet_missing else 'facet.missing=false'
                facets = '%s&%s' % (facets, self.facet_missing)
            if __valid(self.facet_method, self.VALID_FACET_METHODS):
                facets = '%s&facet.method=%s' % (facets, self.facet_method)
        return facets
  
    def __per_field_basis_facet_params(self):
        """
        """
        result = []
        for item in self.facets:
            if 'mincount' in item:
                result.append('f.%s.facet.mincount=%s' %
                        (item['field'], item['mincount']))
            if 'limit' in item:
                result.append('f.%s.facet.limit=%s' %
                        (item['field'], item['limit']))
            if 'sort' in item:
                result.append('f.%s.facet.sort=%s' %
                        (item['field'], urlencode(item['sort'])))
            if 'prefix' in item:
                result.append('f.%s.facet.prefix=%s' %
                        (item['field'], urlencode(item['prefix'])))
            if 'missing' in item:
                temp_missing = 'f.%s.facet.missing=true' % (item['field']) if item['missing'] else 'f.%s.facet.missing=false' % (item['field'])
                result.append(temp_missing)
            if 'method' in item and __valid(item['method'], self.VALID_FACET_METHODS):
                result.append('f.%s.facet.method=%s' %
                        (item['field'], item['method']))
        return '&'.join(result)
    
    def __build_query_facet_dates(self):
        """
        """
        date_facets = ''
        if self.facet_dates != None:
            date_facets = '&'.join(['facet.date=%s' % (facet['field']) for facet in self.facet_dates])
            date_facets = '%s&%s' % (date_facets, self. __per_field_basis_facet_date_params())
            if self.facet_date_start != None:
                date_facets = '%s&facet.date.start=%s' % (date_facets, urlencode(self.facet_date_start))
            if self.facet_date_end != None:
                date_facets = '%s&facet.date.end=%s' % (date_facets, urlencode(self.facet_date_end))
            if self.facet_date_gap != None:
                date_facets = '%s&facet.date.gap=%s' % (date_facets, urlencode(self.facet_date_gap))
            if self.facet_date_hardend != None:
                temp_hardend = 'facet.date.hardend=true' if self.facet_date_hardend else 'facet.date.hardend=false'
                date_facets = '%s&%s' % (date_facets, temp_hardend)
            if __valid(self.facet_date_other, self.VALID_FACET_DATE_OTHERS):
                date_facets = '%s&facet.date.other=%s' % (date_facets, self.facet_date_other)
            if __valid(self.facet_date_include, self.VALID_FACET_DATE_INCLUDES):
                date_facets = '%s&facet.date.include=%s' % (date_facets, self.facet_date_include)
        return date_facets
    
    def __per_field_basis_facet_date_params(self):
        """
        """
        result = []
        for item in self.facet_dates:
            if 'start' in item:
                result.append('f.%s.facet.date.start=%s' % (item['field'], urlencode(item['start'])))
            if 'end' in item:
                result.append('f.%s.facet.date.end=%s' % (item['field'], urlencode(item['end'])))
            if 'gap' in item:
                result.append('f.%s.facet.date.gap=%s' % (item['field'], urlencode(item['gap'])))
            if 'hardend' in item:
                temp_hardend = 'f.%s.facet.date.hardend=true' % (item['field']) if item['hardend'] else 'f.%s.facet.date.hardend=false' % (item['field'])
                result.append(temp_hardend)
            if 'other' in item and __valid(item['other'], self.VALID_FACET_DATE_OTHERS):
                result.append('f.%s.faced.date.other=%s' % (item['field'], item['other']))
            if 'include' in item and __valid(item['include'], self.VALID_FACET_DATE_INCLUDES):
                result.append('f.%s.faced.date.include=%s' % (item['field'], item['include']))
        return '&'.join(result)
    
    def __build_query_facet_ranges(self):
        """
        """
        range_facets = ''
        if self.facet_ranges != None:
            range_facets = '&'.join(['facet.range=%s' % (facet['field']) for facet in self.facet_ranges])
            range_facets = '%s&%s' % (range_facets, self.__per_field_basis_facet_range_params())
            if self.facet_date_start != None:
                range_facets = '%s&facet.range.start=%s' % (range_facets, urlencode(self.facet_range_start))
            if self.facet_date_end != None:
                range_facets = '%s&facet.range.end=%s' % (range_facets, urlencode(self.facet_range_end))
            if self.facet_date_gap != None:
                range_facets = '%s&facet.range.gap=%s' % (range_facets, urlencode(self.facet_range_gap))
            if self.facet_date_hardend != None:
                temp_hardend = 'facet.range.hardend=true' if self.facet_range_hardend else 'facet.range.hardend=false'
                range_facets = '%s&%s' % (range_facets, temp_hardend)
            if __valid(self.facet_range_other, self.VALID_FACET_DATE_OTHERS):
                range_facets = '%s&facet.range.other=%s' % (range_facets, self.facet_range_other)
            if __valid(self.facet_range_include, self.VALID_FACET_DATE_INCLUDES):
                range_facets = '%s&facet.range.include=%s' % (range_facets, self.facet_range_include)
        return range_facets
    
    def __per_field_basis_facet_range_params(self):
        """
        """
        result = []
        for item in self.facet_ranges:
            if 'start' in item:
                result.append('f.%s.facet.range.start=%s' % (item['field'], urlencode(item['start'])))
            if 'end' in item:
                result.append('f.%s.facet.range.end=%s' % (item['field'], urlencode(item['end'])))
            if 'gap' in item:
                result.append('f.%s.facet.range.gap=%s' % (item['field'], urlencode(item['gap'])))
            if 'hardend' in item:
                temp_hardend = 'f.%s.facet.range.hardend=true' % (item['field']) if item['hardend'] else 'f.%s.facet.range.hardend=false' % (item['field'])
                result.append(temp_hardend)
            if 'other' in item and __valid(item['other'], self.VALID_FACET_DATE_OTHERS):
                result.append('f.%s.faced.range.other=%s' % (item['field'], item['other']))
            if 'include' in item and __valid(item['include'], self.VALID_FACET_DATE_INCLUDES):
                result.append('f.%s.faced.range.include=%s' % (item['field'], item['include']))
        return '&'.join(result)
    
    def __build_query_facet_pivots(self):
        """
        """
        facet_pivot = []
        if self.facet_pivot != None:
            facet_pivot = ['facet.pivot=%s' % (','.join(item) for item in self.facet_pivot)]
        return '&'.join(facet_pivot)
    
    def __build_query_facet_queries(self):
        """
        """
        fq = ''
        if self.fq != None:
            fq = '&'.join(['fq=%s' % (urlencode(temp_fq)) for temp_fq in self.fq])
        return fq
    
    def __build_query_return_fields(self):
        """
        """
        fl = ''
        if self.fl != None:
            fl = 'fl=%s' % (','.join(self.fl))
        return fl
    
    def __build_query_sort(self):
        """
        """
        sort = ''
        if self.sort != None:
            sort = {}
            sort['sort'] = self.sort
            sort = urlencode(sort)
        return sort if sort != None else ''
    
    def __build_query_omit_header(self):
        """
        """
        omit_header = ''
        if self.omit_header != None:
            omit_header = 'omitHeader=true' if self.omit_header else 'omitHeader:false'
        return omit_header

def __valid(field, array):
    """
    """
    return (field != None and field in array)